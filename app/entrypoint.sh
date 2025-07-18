case "$RUN_MODE" in
    app)
        uvicorn main:app --host 0.0.0.0
        exit 0
        ;;
    test)
        cd /tmp/
        PYTHONPATH=/usr/src/app pytest --basetemp=/tmp/pytest --cache-clear --rootdir=/usr/src/app /usr/src/app
        exit $?
        ;;
    *)
        exit 1
        ;;
esac
