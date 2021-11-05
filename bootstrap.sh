if [ ! -d "venv/" ]; then
    echo -n "Creating virtual environment directory (venv/)... "
    python3.9 -m venv venv/
    echo "Done!"
fi

source venv/bin/activate
source .env

pip install -r requirements.txt
