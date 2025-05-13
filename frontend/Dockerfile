FROM node:20-bullseye
WORKDIR /app

COPY package*.json ./

# --- work-around ל-npm #4828 ---
RUN npm ci  && \
    rm -rf node_modules package-lock.json && \
    npm install          # ← הסיבוב השני מושך את binary-Rollup

# שאר הקוד
COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
