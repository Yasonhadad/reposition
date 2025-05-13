# frontend/Dockerfile
FROM node:20-bullseye           

WORKDIR /app
COPY package*.json ./

RUN npm ci --omit=optional

COPY . .

RUN npm run build

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
