import pymysql
import yaml
import ipaddress
import sys
import traceback
# estilo
from pyfiglet import Figlet
import tqdm

def read_yaml_config(filename):
    with open(filename, 'r') as file:
        return yaml.safe_load(file)

def connect_to_database(config):
    return pymysql.connect(host=config['host'],
                           user=config['user'],
                           password=config['password'],
                           db=config['db_name'],
                           cursorclass=pymysql.cursors.DictCursor)

def manage_blocks(connection, ipv4_pools):
    with connection.cursor() as cursor:
        for pool in tqdm.tqdm(ipv4_pools, desc='Insertando IPs'):
            network = ipaddress.ip_network(pool['block'])
            pool_name = pool['pool_name']

            ip_exceptions = []
            if 'exceptions' in pool.keys():
                for ip_exception in pool['exceptions']:
                    ip_exceptions.append(ip_exception)

            for ip in tqdm.tqdm(network.hosts(), desc=f'Pool: {pool_name}', leave=False):
                # Verifico si no es una excepcion
                if str(ip) not in ip_exceptions:
                    # Verifica si la IP ya existe en el pool especificado
                    cursor.execute("SELECT * FROM radippool WHERE framedipaddress = %s AND pool_name = %s", (str(ip), pool_name))
                    result = cursor.fetchone()
                    if not result:
                        # Si no existe, inserta la nueva IP con el nombre del pool correspondiente
                        cursor.execute('INSERT INTO radippool (pool_name, framedipaddress, nasipaddress, calledstationid, callingstationid, pool_key) VALUES (%s, %s, "", "", "", "0")', (pool_name, str(ip)))
        connection.commit()

def fprint(text, thefont='standard'):
    flet = Figlet(font=thefont)
    print(flet.renderText(text))

if __name__ == "__main__":
    fprint('Ayuda.LA', )
    print('Script para administrar las IP de los pools de FreeRadius')
    
    config = read_yaml_config('config.yaml')

    db_config = config['database']
    ipv4_pools = config['ipv4_pools']

    connection = connect_to_database(db_config)
    
    try:
        manage_blocks(connection, ipv4_pools)
    except Exception as e:
        print('Excepcion: %s', e)
        sys.exit(1)
    finally:
        connection.close()