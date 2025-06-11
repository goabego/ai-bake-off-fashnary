FROM node:23-slim AS build 
WORKDIR /app
COPY package*.json ./
RUN npm install 

COPY . .

FROM node:23-slim 
WORKDIR /app
COPY --from=build /app/node_modules ./node_modules 
COPY --from=build /app . 

EXPOSE 3000 

CMD ["npm", "run" ,"dev"]