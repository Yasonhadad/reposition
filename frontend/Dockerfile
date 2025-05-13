FROM node:20-bullseye

ENV ROLLUP_FORCE_JS=true \
    ROLLUP_NO_NATIVE=true

WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=optional    

COPY . .


CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
