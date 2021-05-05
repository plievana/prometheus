# 1 - Instalación de prometheus
Instalaremos un prometheus que tendrá acceso a sus propias métricas.
En `etc/prometheus/prometheus.yml` indicamos que haga scraping sobre sus propias métricas.
en http://localhost:9090 tenemos acceso al panel de prometheus
en http://localhost:9090/metrics tenemos acceso a las métricas que scrapea prometheus sobre él mismo

# 2 - Publicación de métricas desde aplicación python
En este segundo ejemplo, creamos una aplicación con `python` y `flask` que publican métricas para que
prometheus las pueda escrapear.
La aplicación la tenemos en http://localhost:5000 y las métricas que registramos en http://localhost:5000/metrics
Estas métricas las publicamos haciendo uso de un middleware para flask proporcionado por el cliente oficial de prometheus para python

Por último, indicamos a prometheus donde tiene que ir a buscar las métricas de la aplicación, editando el fichero `etc/prometheus/prometheus.yml`. Las métricas estarán disponibles con el prefijo `flask_app_`, que es el nombre que hemos utilizado en el código
para definirlas.

Al levantar el stack, podemos acceder a la aplicación en http://localhost:5000
Podemos ver las métricas en http://localhost:5000/metrics
Podemos estas métricas desde prometheus en http://localhost:9090/ y buscando por `flask_app_`

# 3 - Publicación de métricas desde gunicorn
En este tercer ejemplo, creamos una aplicación con `flask` y `python`, corriéndola con `gunicorn`. Para enviar las métricas
de gunicorn a prometheus, nos basaremos en `statsd_exporter`. Nuestra aplicación gunicorn enviará métricas a statsd_exporter
quien a su vez las publicará con un formato conocido para prometheus para que este pueda exportarlas. Para ello, utilizaremos
un exportador de gunicorn para statsd:

    +----------+                         +-------------------+                        +--------------+
    |  StatsD  |---(UDP/TCP repeater)--->|  statsd_exporter  |<---(scrape /metrics)---|  Prometheus  |
    +----------+                         +-------------------+                        +--------------+

para que esto funcione, necesitamos correr el gunicorn con los parámetros `--statsd-host` y `--statsd-prefix`:
- `statsd-host=statsd:9125` -> indicamos el host y el puerto en el que escucha statsd 
- `statsd-prefix=helloworld` -> indicamos el prefijo que vamos a anteponer a todas las métricas.

Configuramos statsd para que publique métricas de códigos de respuesta con el fichero `etc/statsd_exporter/statsd.conf`. En este fichero, tenemos `match: helloworld.gunicorn.request.status.*`. Este `helloworld` tiene que coincidir con el `statsd-prefix` del gunicorn.

Por último, configuramos el prometheus para que vaya al statsd a escrapear las métricas. Esto lo hacemos nuevamente en el fichero `etc/prometheus/prometheus.yml`

Al levantar el stack, podemos acceder a la aplicación en http://localhost:5000 y además tenemos un endpoint http://localhost:5000/wait que hace un sleep de un tiempo random inferior a 1 segundo.
Podemos ver las métricas de statsd en http://localhost:9102/metrics
Podemos estas métricas desde prometheus en http://localhost:9090/ y buscando por `helloworld_`