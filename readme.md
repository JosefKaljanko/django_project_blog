## Django project blog
- jednoduchý projekt

## Spuštění
    cd server
    python manage.py runserver 0.0.0.0:8000

## Zjištění IP
- v terminálu spusť:

      ipconfig   
- Hledej něco jako:
                
      IPv4 Address. . . . . . . . . . . : 192.111.100.14     
- Ulož IP Adresu do .env -> MY_IP_ADRESS


## Access
- http://localhost:8000
- http://127.0.0.1:8000
- http://xxx.xxx.xxx.xx:8000     místo xx nahradit MY_IP_ADRESS

## .env
    DEBUG=True # < or False >
    SECRET_KEY= < Your secret key >

    DB_NAME= < název databaze - vytvoř >
    DB_USER= < Your db user >
    DB_PASSWORD= < Your db password >
    #DB_HOST=localhost
    
    DB_PORT=5432
    DB_HOST=localhost
    
    MY_IP_ADRESS= < Your ip adress (ipconfig) >
