# Simple Place Restaurant Website

A modern, responsive React website for Simple Place restaurant - a Mexican-Vietnamese fusion restaurant in Saigon.

## Features

- 🍕 **Modern React Architecture** - Built with React 18, Vite, and modern JavaScript
- 📱 **Fully Responsive** - Mobile-first design that works on all devices
- 🎨 **Beautiful UI** - Modern design with Tailwind CSS and Framer Motion animations
- 📋 **Dynamic Menu** - Menu items extracted from Excel files and displayed dynamically
- 🍽️ **Booking System** - Complete reservation system with email notifications
- 🚀 **Fast Performance** - Optimized with Vite for lightning-fast development and builds
- ♿ **Accessible** - Built with accessibility best practices

## Pages

- **Home** - Hero section, stats, specials, and restaurant info
- **Menu** - Dynamic menu with search, filtering, and categorization
- **Booking** - Interactive reservation system with email confirmations
- **About** - Restaurant story, team, values, and location info
- **Contact** - Contact form, information, and FAQ section

## Menu Data

The menu items are extracted from Excel files and automatically categorized:
- **Pizza** - 64 items including traditional and fusion pizzas
- **Tacos & Burritos** - 29 items including various taco and burrito options
- **Appetizers** - 17 items including salads, soups, and starters
- **Drinks** - 15 items including beverages and beers
- **Desserts** - 3 items including panna cotta
- **Pasta** - 12 items including spaghetti and penne
- **Other** - 44 items including nachos and extras

## Tech Stack

- **Frontend**: React 18, JSX
- **Backend**: Node.js, Express
- **Email**: Nodemailer with Gmail
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Routing**: React Router DOM
- **Forms**: React Hook Form
- **Icons**: Lucide React
- **Date Handling**: date-fns

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Gmail account for email notifications

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Simple-Place-Website
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install backend dependencies**
   ```bash
   cd server
   npm install
   ```

### Email Setup (Required for Booking System)

1. **Set up Gmail App Password:**
   - Go to your Google Account settings
   - Enable 2-factor authentication
   - Generate an App Password for "Mail"
   - Copy the 16-character password

2. **Configure environment:**
   ```bash
   cd server
   cp env.example .env
   ```
   
   Edit `.env` with your details:
   ```env
   EMAIL_USER=your-email@gmail.com
   EMAIL_PASS=your-16-character-app-password
   RESTAURANT_EMAIL=simpleplace@gmail.com
   ```

### Development

1. **Start the backend server:**
   ```bash
   cd server
   npm run dev
   ```

2. **Start the frontend (in a new terminal):**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:3002`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
Simple-Place-Website/
├── src/                   # Frontend React application
│   ├── components/
│   │   └── Layout.jsx     # Main layout with navigation
│   ├── pages/
│   │   ├── Home.jsx       # Home page
│   │   ├── Menu.jsx       # Menu page with search/filter
│   │   ├── Booking.jsx    # Reservation system with email
│   │   ├── About.jsx      # About page
│   │   └── Contact.jsx    # Contact page
│   ├── App.jsx            # Main app component with routing
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── server/                # Backend API server
│   ├── server.js          # Express server with email functionality
│   ├── package.json       # Backend dependencies
│   ├── env.example        # Environment variables template
│   └── README.md          # Backend setup instructions
├── public/
│   └── menu_data.json     # Menu data from Excel files
└── README.md              # This file
```

## Menu Data Structure

The menu data is stored in `menu_data.json` and contains:

```json
{
  "Pizza": [
    {
      "name": "Item Name",
      "unit": "Phần",
      "price": 150000,
      "source": "source-file.xlsx"
    }
  ]
}
```

## Key Features

### Dynamic Menu System
- Automatically categorizes items from Excel files
- Search and filter functionality
- Responsive grid layout
- Image generation based on item type

### Booking System
- Date and time selection
- Guest count selection
- Form validation with React Hook Form
- **Email notifications** to restaurant and customer
- **Unique booking IDs** for tracking
- **Professional email templates**

### Responsive Design
- Mobile-first approach
- Tailwind CSS for styling
- Framer Motion for smooth animations
- Accessible components

### Performance Optimizations
- Vite for fast development
- Code splitting
- Optimized images
- Lazy loading

## Customization

### Adding New Menu Items
1. Update the Excel files with new items
2. Run the menu extraction script
3. The new items will automatically appear in the menu

### Styling Changes
- Modify `tailwind.config.js` for theme changes
- Update `src/index.css` for global styles
- Component-specific styles are in each component file

### Adding New Pages
1. Create a new component in `src/pages/`
2. Add the route to `src/App.jsx`
3. Update navigation in `src/components/Layout.jsx`

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

For questions about this project, please contact:
- Email: simpleplace@gmail.com
- Phone: (+84) 904421089
- Address: 199F Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh, Vietnam
