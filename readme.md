# Stack for Django Projects by Andres Rojas

- Create alias
    - alias reset_docker='echo "Source .envrc" && source .envrc && echo "Down Docker" && make down && clear && echo "Down Build Docker" && make build && clear && echo "Up Detach" && make up-d'

- Documentacion arquitectura DDD
    - https://www.cosmicpython.com/book/part1.html

- Necesario para iniciar el proyecto
    - crear un role llamado RoleAWSAccess y darle permisos
    - Crear un bucket para guardar los templates
    - Crear la cola sqs en aws y guardarla en la siguiente envs
        -
- obtener access para acceder a los recursos de aws localmente

    - aws sts assume-role --role-arn arn:aws:iam::AWS_ACCOUNT_ID:role/RoleAWSAccess --role-session-name awscli --profile jumpcube --query "Credentials.[AccessKeyId,SecretAccessKey,SessionToken]" --output text | awk '{print "export AWS_ACCESS_KEY_ID="$1"\nexport AWS_SECRET_ACCESS_KEY="$2"\nexport AWS_SECURITY_TOKEN="$3""}' >> .envrc



# Build Fargate

- Error windows push ecr
    - https://stackoverflow.com/questions/60807697/docker-login-error-storing-credentials-the-stub-received-bad-data
        - Remove file docker-credential-wincred.exe C:\Program Files\Docker\Docker\resources\bin
        - Remove "credStore""credsStore"C:\Users\PROFILE_NAME\.docker\config.json
            - C:\Users\andre\.docker
    - O:\AA-DOWNLOAD-D\resources\bin


docker build --no-cache -t django:v1 .

- Probar local
    - docker run -p 8000:8000 django:v1

find . -type f -name "*.Identifier" -exec rm {} +