BASEDIR=$(dirname $0)
CERTDIR='/local2/mnt/qct_auto_programs/grok_info_server/https'
source ${BASEDIR}/venv/bin/activate
cd ${BASEDIR}/opengrok_api
gunicorn --certfile=${CERTDIR}/autom.crt --keyfile=${CERTDIR}/autom.key --bind 0.0.0.0:9999 opengrok_api.wsgi --daemon --reload
#gunicorn --bind 0.0.0.0:9999 opengrok_api.wsgi --daemon --reload
