# frontend/Dockerfile
FROM node:20-bullseye           

WORKDIR /app
COPY package*.json ./

RUN npm ci --omit=optional

COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
