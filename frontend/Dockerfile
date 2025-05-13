FROM node:20-bullseye
WORKDIR /app

ENV ROLLUP_FORCE_JS=true

COPY package*.json ./
RUN npm ci            

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
