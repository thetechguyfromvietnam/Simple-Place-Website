#!/usr/bin/env node

/**
 * Vercel Deployment Setup Script
 * This script helps prepare your Simple Place website for Vercel deployment
 */

import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

console.log('🚀 Simple Place - Vercel Deployment Setup');
console.log('==========================================\n');

// Check if we're in the right directory
const packageJsonPath = path.join(process.cwd(), 'package.json');
if (!fs.existsSync(packageJsonPath)) {
  console.error('❌ Error: package.json not found. Please run this script from the project root.');
  process.exit(1);
}

// Check if git is initialized
try {
  execSync('git status', { stdio: 'ignore' });
  console.log('✅ Git repository detected');
} catch (error) {
  console.log('⚠️  Git repository not initialized. Initializing...');
  try {
    execSync('git init', { stdio: 'inherit' });
    console.log('✅ Git repository initialized');
  } catch (initError) {
    console.error('❌ Failed to initialize git repository');
    process.exit(1);
  }
}

// Check if dependencies are installed
const nodeModulesPath = path.join(process.cwd(), 'node_modules');
if (!fs.existsSync(nodeModulesPath)) {
  console.log('📦 Installing frontend dependencies...');
  try {
    execSync('npm install', { stdio: 'inherit' });
    console.log('✅ Frontend dependencies installed');
  } catch (error) {
    console.error('❌ Failed to install frontend dependencies');
    process.exit(1);
  }
}

// Check server dependencies
const serverNodeModulesPath = path.join(process.cwd(), 'server', 'node_modules');
if (!fs.existsSync(serverNodeModulesPath)) {
  console.log('📦 Installing backend dependencies...');
  try {
    execSync('npm install', { cwd: path.join(process.cwd(), 'server'), stdio: 'inherit' });
    console.log('✅ Backend dependencies installed');
  } catch (error) {
    console.error('❌ Failed to install backend dependencies');
    process.exit(1);
  }
}

// Test build
console.log('🔨 Testing build process...');
try {
  execSync('npm run build', { stdio: 'inherit' });
  console.log('✅ Build successful');
} catch (error) {
  console.error('❌ Build failed. Please fix build errors before deploying.');
  process.exit(1);
}

console.log('\n🎉 Setup completed successfully!');
console.log('\n📋 Next steps:');
console.log('1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)');
console.log('2. Go to vercel.com and create a new project');
console.log('3. Import your Git repository');
console.log('4. Set up environment variables in Vercel dashboard:');
console.log('   - EMAIL_USER=simpleplace199f@gmail.com');
console.log('   - EMAIL_PASS=your-gmail-app-password');
console.log('   - RESTAURANT_EMAIL=simpleplace199f@gmail.com');
console.log('   - FRONTEND_URL=https://your-project-name.vercel.app');
console.log('   - NODE_ENV=production');
console.log('5. Deploy!');
console.log('\n📖 For detailed instructions, see DEPLOYMENT.md');
console.log('\n⚠️  Important: Make sure to set up Gmail App Password before deploying!');
console.log('   See DEPLOYMENT.md for Gmail setup instructions.');
