import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ChevronRight, Star, Users, Clock, MapPin } from 'lucide-react'

const Home = () => {
  const stats = [
    { number: 2000, label: 'Happy Customers', icon: Users },
    { number: 50, label: 'Unique Dishes', icon: Star },
    { number: 5, label: 'Years of Service', icon: Clock },
    { number: 98, label: '% Satisfaction', icon: Star },
  ]

  const features = [
    {
      title: 'Mexico × Vietnam Fusion',
      description: 'A cheerful yellow kitchen famous for pizza topped with taco goodness — elote corn, lemongrass chicken, and fish‑sauce caramel vibes.',
      image: 'https://images.unsplash.com/photo-1600891964599-f61ba0e24092?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80'
    }
  ]

  const specials = [
    {
      title: 'Taco Tuesday',
      description: 'Join us everyday for only 45,000 VND a Tacos',
      schedule: 'Every Tuesday • 10 AM – 10 PM',
      image: '/event-image.jpg'
    },
    {
      title: 'Wednesday Pizza',
      description: '20% Promotion on all pizzas from 10 AM – 10 PM.',
      schedule: 'Offer valid until: September 30, 2025',
      image: '/promo.jpg'
    }
  ]

  return (
    <div className="min-h-screen overflow-hidden">
      {/* Hero Section */}
      <section className="relative isolate h-screen flex items-center justify-center">
        <div 
          className="absolute inset-0 -z-10 parallax-bg bg-cover bg-center"
          style={{ backgroundImage: 'url(/background.jpg)' }}
        />
        <div className="absolute inset-0 -z-10 bg-gradient-to-b from-amber-500/20 via-black/40 to-black/70" />
        
        {/* Floating Elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="floating-element absolute top-20 left-10 text-amber-300 text-6xl opacity-20">🍕</div>
          <div className="floating-element absolute top-40 right-20 text-amber-300 text-4xl opacity-20">🌮</div>
          <div className="floating-element absolute bottom-40 left-20 text-amber-300 text-5xl opacity-20">🌯</div>
        </div>
        
        <div className="text-white">
          <div className="mx-auto max-w-6xl px-4 md:px-8 lg:px-12 py-24 md:py-36">
            <motion.div
              initial={{ opacity: 0, x: -100 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="inline-block text-xs uppercase tracking-widest text-amber-300"
            >
              Mexico × Vietnam
            </motion.div>
            <motion.h1 
              initial={{ opacity: 0, x: -100 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-4xl md:text-6xl font-semibold leading-tight mt-4"
            >
              Homemade pizza, taco soul.
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, x: -100 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="text-white/90 mt-4 md:text-lg max-w-2xl"
            >
              A cheerful yellow kitchen famous for pizza topped with taco goodness — elote corn, lemongrass chicken, and fish‑sauce caramel vibes.
            </motion.p>
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="mt-8 flex flex-col sm:flex-row gap-3"
            >
              <Link 
                to="/booking"
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
              >
                Book a table
              </Link>
              <Link 
                to="/menu"
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-white/70 text-white hover:bg-white/10"
              >
                See menu
              </Link>
              <Link 
                to="/menu"
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-white text-amber-700 hover:bg-amber-50 inline-flex items-center gap-2"
              >
                View Menu <ChevronRight size={16} />
              </Link>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.0 }}
              className="mt-5 text-sm text-amber-200"
            >
              Open today: 11:00–22:00
            </motion.div>
          </div>
        </div>
        {/* Wave divider */}
        <svg className="-mb-1 w-full text-neutral-50" viewBox="0 0 1440 80" fill="currentColor" aria-hidden="true">
          <path d="M0,32L80,26.7C160,21,320,11,480,21.3C640,32,800,64,960,69.3C1120,75,1280,53,1360,42.7L1440,32L1440,80L1360,80C1280,80,1120,80,960,80C800,80,640,80,480,80C320,80,160,80,80,80L0,80Z" />
        </svg>
      </section>

      {/* Stats Section */}
      <section className="px-4 md:px-8 lg:px-12 py-16 bg-gradient-to-r from-amber-50 to-yellow-50">
        <div className="mx-auto max-w-6xl">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <motion.div 
                  key={stat.label}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="stat-item"
                >
                  <div className="text-4xl md:text-5xl font-bold text-amber-600 stat-number flex items-center justify-center gap-2">
                    <Icon size={32} />
                    {stat.number.toLocaleString()}
                  </div>
                  <div className="text-sm text-neutral-600 mt-2">{stat.label}</div>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Specials Banner */}
      <section className="px-4 md:px-8 lg:px-12 py-8">
        <div className="mx-auto max-w-6xl">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="specials-banner rounded-2xl shadow-lg p-5 md:p-6 flex flex-col md:flex-row md:items-center md:justify-between gap-3"
          >
            <div>
              <h2 className="text-2xl md:text-3xl font-semibold text-amber-800">Pizza × Tacos Weekly Specials</h2>
              <p className="text-amber-700">Ask for the Saigon Elote or the Bánh Mì Supreme this week.</p>
            </div>
            <div className="flex gap-2">
              <Link 
                to="/menu"
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600"
              >
                View Menu
              </Link>
              <Link 
                to="/booking"
                className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition border border-amber-500 text-amber-700 hover:bg-amber-50"
              >
                Reserve
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* About Section */}
      <section className="px-4 md:px-8 lg:px-12 py-16">
        <div className="mx-auto max-w-6xl">
          {features.map((feature, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="grid gap-8 md:grid-cols-2 items-center"
            >
              <div className="rounded-3xl h-72 md:h-96 bg-gradient-to-br from-amber-100 to-yellow-100 shadow-lg flex items-center justify-center relative overflow-hidden">
                <img 
                  src={feature.image} 
                  alt="Restaurant Kitchen" 
                  className="w-full h-full object-cover rounded-3xl" 
                />
                <div className="absolute inset-0 opacity-10">
                  <div className="absolute top-4 left-4 text-2xl">🍕</div>
                  <div className="absolute top-8 right-8 text-xl">🌮</div>
                  <div className="absolute bottom-8 left-8 text-xl">🌶️</div>
                </div>
              </div>
              <div>
                <h3 className="text-2xl md:text-3xl font-semibold mb-3">Our Story</h3>
                <p className="text-neutral-700 leading-relaxed">{feature.description}</p>
                <div className="mt-4 flex items-center gap-2 text-amber-600" aria-label="5 out of 5 stars">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} size={20} className="hover:scale-110 transition-transform fill-current" />
                  ))}
                  <span className="text-sm text-neutral-500 ml-2">Loved by 2,000+ diners</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Events & Promotions */}
      <section className="px-4 md:px-8 lg:px-12 py-16 bg-yellow-50">
        <div className="mx-auto max-w-6xl">
          <motion.h2 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-2xl font-bold text-center text-amber-700 mb-8"
          >
            Events & Promotions
          </motion.h2>
          <div className="grid gap-6 md:grid-cols-2">
            {specials.map((special, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="rounded-2xl border bg-white shadow hover:shadow-lg transition-shadow"
              >
                <img 
                  src={special.image} 
                  alt={special.title} 
                  className="rounded-t-2xl w-full h-48 object-cover" 
                />
                <div className="p-5">
                  <h3 className="font-semibold text-lg text-amber-700">{special.title}</h3>
                  <p className="text-sm text-neutral-600 mt-2">{special.description}</p>
                  <p className="text-sm text-neutral-800 font-medium mt-3">{special.schedule}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Visit Section */}
      <section className="px-4 md:px-8 lg:px-12 py-16">
        <div className="mx-auto max-w-6xl">
          <div className="grid gap-8 md:grid-cols-2">
            {/* Hours Card */}
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="rounded-2xl border bg-white hover:shadow-xl transition-shadow"
            >
              <div className="p-6 border-b flex items-center gap-2">
                <Clock className="text-amber-600" size={20} />
                <h4 className="font-semibold text-lg">Hours</h4>
              </div>
              <div className="p-6 text-sm">
                <p className="text-neutral-600 mb-4">Walk-ins welcome • Reservations recommended on weekends</p>
                <div className="grid grid-cols-2 gap-y-3">
                  <div>
                    <div className="font-medium">Mon–Thu</div>
                    <div className="text-neutral-700">11:00 – 22:00</div>
                  </div>
                  <div>
                    <div className="font-medium">Fri</div>
                    <div className="text-neutral-700">11:00 – 23:00</div>
                  </div>
                  <div>
                    <div className="font-medium">Sat</div>
                    <div className="text-neutral-700">10:00 – 23:00</div>
                  </div>
                  <div>
                    <div className="font-medium">Sun</div>
                    <div className="text-neutral-700">10:00 – 21:00</div>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Location Card */}
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
              viewport={{ once: true }}
              className="rounded-2xl border bg-white hover:shadow-lg transition-shadow"
            >
              <div className="p-5 border-b">
                <div className="flex items-center gap-2">
                  <MapPin className="text-amber-600" size={20} />
                  <h4 className="font-semibold">Location</h4>
                </div>
                <p className="text-sm text-neutral-600">199F Nguyễn Văn Hưởng, Thảo Điền, Quận 2, Hồ Chí Minh, Vietnam</p>
              </div>
              <div className="aspect-[16/10] w-full overflow-hidden rounded-xl shadow">
                <iframe 
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3918.9736309123427!2d106.7310951750612!3d10.813329758511895!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x317527df16b4efab%3A0x7e7862d6d7c4818b!2sSimple%20Place!5e0!3m2!1sen!2s!4v1756970263264!5m2!1sen!2s" 
                  width="600" 
                  height="450" 
                  style={{ border: 0 }} 
                  allowFullScreen="" 
                  loading="lazy" 
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Simple Place Location"
                />
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
