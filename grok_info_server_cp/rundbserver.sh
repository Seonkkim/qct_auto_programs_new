BASEDIR=$(dirname $0)
CERTDIR=https
source ${BASEDIR}/venv/bin/activate
cd ${BASEDIR}/opengrok_api
gunicorn --certfile=/local2/mnt/qct_auto_programs/grok_info_server/${CERTDIR}/automotive.crt --keyfile=/local2/mnt/qct_auto_programs/grok_info_server/${CERTDIR}/auto.key --bind 0.0.0.0:9998 opengrok_api.wsgi --reload --daemon
#gunicorn --bind 0.0.0.0:9999 opengrok_api.wsgi --daemon --reload
