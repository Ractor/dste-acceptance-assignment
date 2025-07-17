case "$RUN_MODE" in
    app)
        uvicorn main:app --host 0.0.0.0
        exit 0
        ;;
    training)
        python ./housing/model.py
        exit 0
        ;;
    *)
        exit 1
        ;;
esac
