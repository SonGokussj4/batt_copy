#!/bin/bash

## jverner POCITADLO
/expSW/SOFTWARE/bin/pocitadlo

## FIND DIRECTORY OF THE SCRIPT
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do  # resolve $SOURCE until the file is no longer a symlink
  SCRIPTDIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  # if $SOURCE was a relative symlink, we need to resolve it
  # relative to the path where the symlink file was located
  [[ $SOURCE != /* ]] && SOURCE="$SCRIPTDIR/$SOURCE"
done
SCRIPTDIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null && pwd )"

## ACTIVATE VIRTUAL ENVIRONMENT AND RUN APP
source "$SCRIPTDIR"/.venv/bin/activate
scriptname=$(basename ${SCRIPTDIR})
python "${SCRIPTDIR}/${scriptname}/${scriptname}.py" "$@"
