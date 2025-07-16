case "$RUN_MODE" in
    model)
        python ./main.py
        exit 0
        ;;
    *)
        exit 1
        ;;
esac
