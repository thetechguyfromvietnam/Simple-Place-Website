#!/usr/bin/env node

/**
 * Gmail Email Test Script
 * Tests Gmail authentication and email sending
 */

import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

console.log('📧 Gmail Email Test');
console.log('==================\n');

// Check environment variables
console.log('Environment Variables:');
console.log(`EMAIL_USER: ${process.env.EMAIL_USER || 'NOT SET'}`);
console.log(`EMAIL_PASS: ${process.env.EMAIL_PASS ? 'SET (hidden)' : 'NOT SET'}`);
console.log(`RESTAURANT_EMAIL: ${process.env.RESTAURANT_EMAIL || 'NOT SET'}\n`);

if (!process.env.EMAIL_USER || !process.env.EMAIL_PASS) {
  console.log('❌ Missing required environment variables');
  console.log('Please set EMAIL_USER and EMAIL_PASS');
  process.exit(1);
}

// Create transporter
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
});

// Test email
const testEmail = {
  from: process.env.EMAIL_USER,
  to: process.env.RESTAURANT_EMAIL || process.env.EMAIL_USER,
  subject: 'Simple Place - Email Test',
  html: `
    <h2>✅ Email Test Successful!</h2>
    <p>This is a test email from Simple Place restaurant website.</p>
    <p><strong>Timestamp:</strong> ${new Date().toISOString()}</p>
    <p>If you receive this email, your Gmail configuration is working correctly!</p>
  `
};

console.log('Sending test email...');

transporter.sendMail(testEmail)
  .then(() => {
    console.log('✅ Email sent successfully!');
    console.log('Check your inbox for the test email.');
  })
  .catch((error) => {
    console.log('❌ Email failed to send:');
    console.log('Error:', error.message);
    
    if (error.message.includes('BadCredentials')) {
      console.log('\n🔧 BadCredentials Fix:');
      console.log('1. Make sure 2FA is enabled on your Gmail account');
      console.log('2. Generate a new App Password:');
      console.log('   https://myaccount.google.com/apppasswords');
      console.log('3. Use the App Password (16 characters, no spaces)');
      console.log('4. Update EMAIL_PASS in Vercel environment variables');
    }
  });
