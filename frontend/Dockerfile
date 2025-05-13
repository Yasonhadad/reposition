FROM node:20-bullseye
WORKDIR /app

# ✔️ מביא את Rollup לעבוד בג׳אווה-סקריפט בלבד
ENV ROLLUP_FORCE_JS=true

COPY package*.json ./
RUN npm ci            # התקנה רגילה – לא מדלגים על optional

COPY . .

# dev-server של Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
