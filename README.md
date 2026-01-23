# Simple Place Website

Modern Next.js website for Simple Place restaurant with booking system and menu management.

## Features

- 🍕 **Full Menu Display** - Complete menu with categories and filtering
- 📅 **Table Reservation** - Booking system with email notifications
- 🎨 **Modern UI/UX** - Beautiful animations and responsive design
- ⚡ **Fast Performance** - Optimized with Next.js 14 and TypeScript
- 📱 **Mobile First** - Fully responsive design
- 🎯 **Best Sellers** - Featured items highlighting

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: AOS (Animate On Scroll) + Framer Motion
- **Deployment**: Vercel
- **Data**: JSON files for menu management

## Setup

1. **Install dependencies**:
```bash
npm install
```

2. **Set up environment variables**:
Create a `.env.local` file:
```env
NOTIFICATION_EMAIL=your-email@gmail.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

📖 **Xem hướng dẫn chi tiết**: [EMAIL_SETUP.md](./EMAIL_SETUP.md)

3. **Run development server**:
```bash
npm run dev
```

4. **Build for production**:
```bash
npm run build
npm start
```

## Email Notification Setup

Hệ thống tự động gửi email thông báo lên điện thoại khi có booking mới.

📖 **Xem hướng dẫn chi tiết**: [EMAIL_SETUP.md](./EMAIL_SETUP.md)

**Tóm tắt:**
1. Tạo App Password cho Gmail (nếu dùng Gmail)
2. Cấu hình SMTP settings trong `.env.local`
3. Bật push notification trên app email của điện thoại

Email sẽ chứa đầy đủ thông tin booking: Tên khách hàng, Email, Số điện thoại, Ngày giờ, Số khách, Ghi chú

✅ **Ưu điểm**: Đơn giản, miễn phí, notification nhanh trên điện thoại!

## Deployment to Vercel

📖 **Xem hướng dẫn chi tiết**: [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md)

**Tóm tắt:**
1. Push code to GitHub
2. Import project to Vercel
3. **Thêm các Environment Variables sau vào Vercel:**
   - `NOTIFICATION_EMAIL` = `simpleplace199f@gmail.com`
   - `SMTP_HOST` = `smtp.gmail.com`
   - `SMTP_PORT` = `587`
   - `SMTP_USER` = `simpleplace199f@gmail.com`
   - `SMTP_PASSWORD` = `bkmh yygs tdvd fahv`
4. Redeploy!

## Project Structure

```
├── app/
│   ├── api/
│   │   └── booking/        # Booking API route
│   ├── components/         # React components
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── data/
│   └── menu.json          # Menu data
├── public/
│   └── images/            # Static images
├── EMAIL_SETUP.md         # Hướng dẫn setup email notification
├── VERCEL_DEPLOY.md       # Hướng dẫn deploy lên Vercel
└── vercel.json            # Vercel configuration
```

## License

© 2025 Simple Place. All rights reserved.
