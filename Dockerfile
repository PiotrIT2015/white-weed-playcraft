# ETAP 1: Budowanie (musisz dodać "AS build")
FROM node:20-alpine AS build
WORKDIR /app

# Kopiujemy pliki konfiguracyjne
COPY package*.json ./
COPY frontend/package*.json ./frontend/

# Instalujemy zależności
RUN npm install

# Kopiujemy resztę plików
COPY . .

# Uruchamiamy budowanie (korzystając ze skryptu, który poprawiliśmy w package.json)
RUN npm run build

# ETAP 2: Serwowanie przez Nginx
FROM nginx:alpine

# Kopiujemy zbudowane pliki z etapu o nazwie "build"
# UWAGA: Jeśli używasz React, zmień 'dist' na 'build' poniżej
COPY --from=build /app/frontend/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]






