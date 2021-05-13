#!/bin/bash

# Docker
export COMPOSE_PROJECT_NAME="accpy-oidc-server"


if [ ! -z "${ACAPY_ADMIN_URL_API_KEY}" ]; then
  ACAPY_ADMIN_MODE="admin-api-key ${ACAPY_ADMIN_URL_API_KEY}"
fi

function echoError (){
  _msg=${1}
  _red='\e[31m'
  _nc='\e[0m' # No Color
  echo -e "${_red}${_msg}${_nc}"
}

function echoWarning (){
  _msg=${1}
  _yellow='\e[33m'
  _nc='\e[0m' # No Color
  echo -e "${_yellow}${_msg}${_nc}"
}

function echoRed (){
  _msg=${1}
  _red='\e[31m'
  _nc='\e[0m' # No Color
  echo -e "${_red}${_msg}${_nc}"
}

function echoYellow (){
  _msg=${1}
  _yellow='\e[33m'
  _nc='\e[0m' # No Color
  echo -e "${_yellow}${_msg}${_nc}"
}

function isCurlInstalled () {
  CURL_EXE=curl
  if ! isInstalled ${CURL_EXE}; then
    echoError "The ${CURL_EXE} executable is required and was not found on your path."
    echoError "If your shell of choice doesn't come with curl preinstalled, try installing it using either [Homebrew](https://brew.sh/) (MAC) or [Chocolatey](https://chocolatey.org/) (Windows)."
    exit 1
  fi
}

function isInstalled () {
  rtnVal=$(type "$1" >/dev/null 2>&1)
  rtnCd=$?
  if [ ${rtnCd} -ne 0 ]; then
    return 1
  else
    return 0
  fi
}

function isJQInstalled () {
  JQ_EXE=jq
  if ! isInstalled ${JQ_EXE}; then
    echoError "The ${JQ_EXE} executable is required and was not found on your path."
    echoError "Installation instructions can be found here: https://stedolan.github.io/jq/download"
    echoError "Alternatively, a package manager such as Chocolatey (Windows) or Brew (Mac) can be used to install this dependecy."
    exit 1
  fi
}

function isNgrokInstalled () {
  NGROK_EXE=ngrok
  if ! isInstalled ${NGROK_EXE}; then
    echoError "The ${NGROK_EXE} executable is needed and not on your path."
    echoError "It can be downloaded from here: https://ngrok.com/download"
    echoError "Alternatively, a package manager such as Chocolatey (Windows) or Brew (Mac) can be used to install this dependecy."
    exit 1
  fi
}

start() {
    isJQInstalled
    isCurlInstalled
    isNgrokInstalled

    # Set environment variables for ngrok
    if [ -z "$NGROK_CONTROLLER_URL" ]; then

      export NGROK_CONTROLLER_URL=$(${CURL_EXE} http://localhost:4040/api/tunnels | ${JQ_EXE} --raw-output '.tunnels | map(select(.name | contains("vc-authn-controller"))) | .[0] | .public_url')
    fi
    if [ -z "$NGROK_CONTROLLER_URL" ]; then
      echoError "The NGROK_CONTROLLER_URL has not been set. Start ngrok with ./scripts/start-ngrok.sh"
      exit 1
    fi

    export SITE_URL=${NGROK_CONTROLLER_URL}

    echo "Running in demo mode, will use ${NGROK_CONTROLLER_URL} for the controller endpoint."

    if [ -z "$NGROK_AGENT_URL" ]; then
      export NGROK_AGENT_URL=$(${CURL_EXE} http://localhost:4040/api/tunnels | ${JQ_EXE} --raw-output '.tunnels | map(select(.name | contains("vc-authn-agent"))) | .[0] | .public_url')
    fi
    if [ -z "$NGROK_AGENT_URL" ]; then
      echoError "The NGROK_AGENT_URL has not been set. Start ngrok with ./scripts/start-ngrok.sh"
      exit 1
    fi

    echo "Running in demo mode, will use ${NGROK_AGENT_URL} for the agent endpoint."

    # Update webhook link below to match ngrok port 5000 URL
    export IDENTITY_SERVER_URL="${IDENTITY_SERVER_URL:-$NGROK_CONTROLLER_URL}"
#    echo "${IDENTITY_SERVER_URL}"
    export IDENTITY_SERVER_API_KEY=""
    export IDENTITY_SERVER_WEB_HOOK_URL=${IDENTITY_SERVER_WEB_HOOK_URL:-$NGROK_CONTROLLER_URL/webhooks}
#    echo "${IDENTITY_SERVER_WEB_HOOK_URL}"

    NGROK_CONTROLLER_URL_STRIPPED=`echo $NGROK_CONTROLLER_URL | sed 's/https:\/\///g'`
    echo "${NGROK_CONTROLLER_URL}/vc/connect/authorize/?pres_req_conf_id=verified-email&scope=openid+profile+vc_authn&response_type=code&client_id=531136&redirect_uri=https%3A%2F%2F${NGROK_CONTROLLER_URL_STRIPPED}%2Foidc%2Fauth%2Fcb%2F&state=O8ALJmGFm5ByvYMyWhT7vkzdc3dc5Yds&nonce="

    export AUTH_URL="${NGROK_CONTROLLER_URL}/vc/connect/authorize/?pres_req_conf_id=verified-email&scope=openid+profile+vc_authn&response_type=code&client_id=531136&redirect_uri=https%3A%2F%2F${NGROK_CONTROLLER_URL_STRIPPED}%2Foidc%2Fauth%2Fcb%2F&state=O8ALJmGFm5ByvYMyWhT7vkzdc3dc5Yds&nonce="
    docker-compose build
    docker-compose -p ${COMPOSE_PROJECT_NAME} up -d
    docker-compose logs -f
}
stop() {
    docker-compose -p ${COMPOSE_PROJECT_NAME} stop
}

usage() {
    echo "$0 start | stop"
}

COMMAND=${1}

case "${COMMAND}" in
start)
     start
     ;;
stop)
     stop
     ;;
*)
     usage
     ;;
esac
     
     