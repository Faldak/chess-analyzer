echo #!/bin/bash > setup.sh
echo apt-get update -y >> setup.sh
echo apt-get install -y wget >> setup.sh
echo wget -q https://github.com/official-stockfish/Stockfish/releases/download/sf_17/stockfish-ubuntu-x86-64.tar >> setup.sh
echo tar -xf stockfish-ubuntu-x86-64.tar >> setup.sh
echo mv stockfish/stockfish-ubuntu-x86-64 /usr/local/bin/stockfish >> setup.sh
echo chmod +x /usr/local/bin/stockfish >> setup.sh