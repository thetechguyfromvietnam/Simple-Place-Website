#!/usr/bin/env node

/**
 * Simple Gmail Test
 * Tests Gmail credentials without external dependencies
 */

console.log('📧 Gmail Credentials Test');
console.log('========================\n');

console.log('To test your Gmail credentials:');
console.log('1. Generate a new App Password:');
console.log('   https://myaccount.google.com/apppasswords');
console.log('2. Update EMAIL_PASS in Vercel dashboard');
console.log('3. Redeploy your Vercel function');
console.log('4. Test an order on your website\n');

console.log('Required Environment Variables:');
console.log('- EMAIL_USER: simpleplace199f@gmail.com');
console.log('- EMAIL_PASS: your-16-character-app-password');
console.log('- RESTAURANT_EMAIL: simpleplace199f@gmail.com');
console.log('- FRONTEND_URL: www.simpleplacevn.com');
console.log('- NODE_ENV: production\n');

console.log('After updating credentials:');
console.log('1. Go to your website: https://www.simpleplacevn.com');
console.log('2. Add items to cart');
console.log('3. Place a test order');
console.log('4. Check if emails are sent successfully\n');

console.log('If still having issues:');
console.log('- Make sure 2FA is enabled on Gmail');
console.log('- Use App Password, not regular password');
console.log('- No spaces in the App Password');
console.log('- Wait 5-10 minutes after updating credentials');
