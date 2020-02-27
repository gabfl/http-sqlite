# http-sqlite

[![Build Status](https://travis-ci.org/gabfl/http-sqlite.svg?branch=master)](https://travis-ci.org/gabfl/http-sqlite)
[![codecov](https://codecov.io/gh/gabfl/http-sqlite/branch/master/graph/badge.svg)](https://codecov.io/gh/gabfl/http-sqlite)
[![MIT licensed](https://img.shields.io/badge/license-MIT-green.svg)](https://raw.githubusercontent.com/gabfl/http-sqlite/master/LICENSE)

`http-sqlite` is a rest API built on top of SQLite.

It simply allows users to run any SQLite query over HTTP.

## Authentication

The rest API is authenticated with a header `X-Auth-Token`.

When launching `http-sqlite` for the first time a file `src/data/token` is automatically created with a random token.

You can override the file content to choose a personalized token.

## Usage example

### Checking SQLite version

```bash
curl http://127.0.0.1:5000/ \
 --header "X-Auth-Token: ****" \
 --data "SELECT sqlite_version();"
{
  "message": null, 
  "result": [
    [
      "3.30.1"
    ]
  ], 
  "success": true
}
```

### Creating a table

```bash
curl http://127.0.0.1:5000/ \
 --header "X-Auth-Token: ****" \
 --data "CREATE TABLE test (t text, d date)"
```

```json
{
  "message": null, 
  "result": [], 
  "success": true
}
```

### Inserting rows

```bash
curl http://127.0.0.1:5000/ \
 --header "X-Auth-Token: ****" \
 --data "INSERT INTO test (t, d) VALUES ('Some text', date('now'))"
```

```json
{
  "message": null, 
  "result": [], 
  "success": true
}
```

### Selecting rows from a table

```bash
curl http://127.0.0.1:5000/ \
 --header "X-Auth-Token: ****" \
 --data "SELECT * FROM test;"
 ```

```json
{
  "message": null, 
  "result": [
    [
      "Some text", 
      "2020-02-27"
    ], 
    [
      "Some other text", 
      "2020-02-27"
    ]
  ], 
  "success": true
}
```

### CSV support

#### Retrieve output as a CSV

```bash
curl http://127.0.0.1:5000/to_csv \
 --header "X-Auth-Token: ****" \
 --data "SELECT * FROM test;"
 ```

 ```json
Some text,2020-02-27
Some other text,2020-02-27
 ```

## Installation

```bash
$ cd http-sqlite/
$ pip3 install -r requirements.txt
$ python3 -m src
```
