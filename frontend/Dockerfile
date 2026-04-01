FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM httpd:2.4-alpine
RUN rm -rf /usr/local/apache2/htdocs/*
COPY --from=build /app/build/ /usr/local/apache2/htdocs/









