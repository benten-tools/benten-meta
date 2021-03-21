# benten-meta
BENTEN metadata tool



## Summary

This provides metadata tools for benten metadata format.

BENTEN provides two ways to present metadata.  

* metadata with flat key, json  ( "@" is used to provide flat key to present hierarchical metadata)

```
{
    "@data_info@identifier@pid":"facility.xxxxx",
    "@data_info@identifier@proposal_number":"xxxxx"
}
```

* hierarchical metadata, yaml

```
data_info:
  identifier:
    pid: facility.xxxxx
    proposal_number: xxxxx
```

  This tool can convert metadata from json to yaml, or from yaml to json.

## Install

```
$ pip install benten-meta
```

## Usage

* convert metadata from yaml to json

```
$　benten-meta.py convert_yaml2json example/metadata_hierarchy.yml test_flat.json
### benten-meta convert_yaml2json ###
==> convert from example/metadata_hierarchy.yml into test_flat.json
```

* convert metadata from json to yaml

```
$ benten-meta.py convert_json2yaml example/metadata_flat.json test_hierarchy.yml 
### benten-meta convert_json2yaml ###
==> convert from example/metadata_flat.json into test_hierarchy.yml
```

## License

Apache License 2.0

## Author

Copyright (C) 2021 Takahiro Matsumoto (matumot@spring8.or.jp)