# ==============================================================================
# EchoMesh AI Frontend Dockerfile
# ==============================================================================

FROM node:18-alpine

WORKDIR /app

# Install dependencies based on preferred package manager
COPY package.json ./

RUN npm install

COPY . .

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Start Next.js development server
CMD ["npm", "run", "dev"]
