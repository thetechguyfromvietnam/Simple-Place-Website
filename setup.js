#!/usr/bin/env node

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log('🚀 Setting up Simple Place Website...\n');

// Check if Node.js version is compatible
const nodeVersion = process.version;
const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);

if (majorVersion < 16) {
  console.error('❌ Node.js 16 or higher is required. Current version:', nodeVersion);
  process.exit(1);
}

console.log('✅ Node.js version check passed:', nodeVersion);

try {
  // Install frontend dependencies
  console.log('\n📦 Installing frontend dependencies...');
  execSync('npm install', { stdio: 'inherit' });
  
  // Install backend dependencies
  console.log('\n📦 Installing backend dependencies...');
  execSync('cd server && npm install', { stdio: 'inherit' });
  
  // Create .env file if it doesn't exist
  const envPath = path.join('server', '.env');
  const envExamplePath = path.join('server', 'env.example');
  
  if (!fs.existsSync(envPath) && fs.existsSync(envExamplePath)) {
    console.log('\n📧 Creating environment file...');
    fs.copyFileSync(envExamplePath, envPath);
    console.log('✅ Created server/.env file');
    console.log('⚠️  Please update server/.env with your email credentials');
  }
  
  console.log('\n🎉 Setup complete!');
  console.log('\n📋 Next steps:');
  console.log('1. Update server/.env with your Gmail credentials');
  console.log('2. Start the backend: cd server && npm run dev');
  console.log('3. Start the frontend: npm run dev');
  console.log('4. Open http://localhost:3000 in your browser');
  
} catch (error) {
  console.error('❌ Setup failed:', error.message);
  process.exit(1);
}
