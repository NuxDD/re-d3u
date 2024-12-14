# Dump
DUMPER_PATH=$1
DUMP_OUTPUT_PATH=./dump_output/

# D3U
D3U_PATH=$2
METADATA_PATH=$D3U_PATH/Dofus_data/il2cpp_data/Metadata/global-metadata.dat

# Decompiler
DECOMPILER_PATH=~/.dotnet/tools/ilspycmd
GAME_DECOMP_DIR=./re/Ankama.Protocol.Game
CONNECTION_DECOMP_DIR=./re/Ankama.Protocol.Connection

# Only work for Linux, .dll for windows is required ?
wine $DUMPER_PATH $D3U_PATH/GameAssembly.so $METADATA_PATH $DUMP_OUTPUT_PATH

rm -rf $GAME_DECOMP_DIR/*
rm -rf $CONNECTION_DECOMP_DIR/*

$DECOMPILER_PATH -p -o $GAME_DECOMP_DIR $DUMP_OUTPUT_PATH/DummyDll/Ankama.Dofus.Protocol.Game.dll  
$DECOMPILER_PATH -p -o $CONNECTION_DECOMP_DIR $DUMP_OUTPUT_PATH/DummyDll/Ankama.Dofus.Protocol.Connection.dll  

rm -rf $DUMP_OUTPUT_PATH/
