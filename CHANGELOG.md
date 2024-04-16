#Changelog


## [1.0.2] - 16.04.2024
- build wheel in CI and distribute Alpine friendly wheels for internal CLARIN
  use
- new API endpoint `/expanddatatype?data_type=<data_type>` (not operational yet)
- fetch includes `/expanddatatype` response by default

## [1.0.1] - never released
Changes:
- Fixed stability issue by providing shared cache for uwsgi apps
- `dogui` Django raw HTML templates
- Unittests for parameter parsing
- Fixed CI pipeline
- Build config with `.toml + Poetry`
- Unittests for endpoints
- OpenAPI 3.0 endpoint documentation
- Upgrade Python==3.11 and Django==4.2
- Fix whitespaces in PID form breaking DOG
- Replace `{**A, **B}` to Python >=3.9 `A | B`

## [1.0.0] - 17.11.2022
First release of Digital Object Gate web application
- Expose DOGlib functionality as REST API microservice

