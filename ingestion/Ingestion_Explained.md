ingestion/

This folder is for the dockerfiles. The scripts the docker files run are found in the scripts folder.

# csv-parquet-ingester
## build image
`docker build -t csv-parquet-ingester .`

## run container
``` 
docker run \
    --network pg-network \
    csv-parquet-ingester \
    --schema project_name \
    --tb table_name \
    --url "file.csv"
```

# json-ingester
## build image
`docker build -t json-ingester .`

## run container
```
docker run -v /path/to/your/json:/app/data json-ingester \
  --schema your_schema \
  --table your_table \
  --file_path /app/data/your_file.json
```

