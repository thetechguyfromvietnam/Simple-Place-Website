import { motion } from 'framer-motion'
import { Star, Users, Clock, MapPin, Heart, Award } from 'lucide-react'

const About = () => {
  const stats = [
    { number: 2000, label: 'Happy Customers', icon: Users },
    { number: 50, label: 'Unique Dishes', icon: Award },
    { number: 5, label: 'Years of Service', icon: Clock },
    { number: 98, label: '% Satisfaction', icon: Heart },
  ]

  const values = [
    {
      icon: Heart,
      title: 'Passion for Food',
      description: 'We pour our heart into every dish, combining authentic Mexican and Vietnamese flavors with modern techniques.'
    },
    {
      icon: Users,
      title: 'Community First',
      description: 'We believe in bringing people together through great food and warm hospitality in our cozy yellow space.'
    },
    {
      icon: Award,
      title: 'Quality Ingredients',
      description: 'We source the freshest ingredients and prepare everything with care, from our homemade dough to our signature sauces.'
    },
    {
      icon: Star,
      title: 'Innovation',
      description: 'We constantly experiment with new fusion combinations while respecting traditional cooking methods.'
    }
  ]

  const team = [
    {
      name: 'Maria Rodriguez',
      role: 'Head Chef & Co-Founder',
      image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?q=80&w=400&auto=format&fit=crop',
      bio: 'Maria brings 15 years of Mexican culinary expertise to Simple Place, creating authentic flavors with a modern twist.'
    },
    {
      name: 'Nguyen Minh',
      role: 'Co-Founder & Operations',
      image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400&auto=format&fit=crop',
      bio: 'Minh manages our daily operations and ensures every customer leaves with a smile and a full stomach.'
    },
    {
      name: 'Carlos Silva',
      role: 'Pizza Specialist',
      image: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?q=80&w=400&auto=format&fit=crop',
      bio: 'Carlos crafts our artisanal pizzas with traditional Italian techniques and Vietnamese-inspired toppings.'
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50">
      {/* Hero Section */}
      <section className="relative py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center mb-16"
          >
            <h1 className="text-5xl font-bold text-gray-900 mb-6">Our Story</h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Simple Place started as a dream to bring together the vibrant flavors of Mexico and Vietnam 
              in one welcoming space. What began as a tiny home kitchen has grown into Saigon's favorite 
              fusion restaurant.
            </p>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16"
          >
            {stats.map((stat, index) => {
              const Icon = stat.icon
              return (
                <div key={stat.label} className="text-center">
                  <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                    <Icon className="text-amber-500 mx-auto mb-3" size={32} />
                    <div className="text-3xl font-bold text-gray-900 mb-2">
                      {stat.number.toLocaleString()}
                    </div>
                    <div className="text-sm text-gray-600">{stat.label}</div>
                  </div>
                </div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* Our Story Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-3xl font-bold text-gray-900 mb-6">How It All Began</h2>
              <div className="space-y-4 text-gray-600 leading-relaxed">
                <p>
                  In 2019, Maria and Minh met at a food market in District 2, bonding over their shared 
                  passion for authentic flavors and community. Maria, a Mexican expat, missed the taste 
                  of home, while Minh wanted to introduce Vietnamese culinary traditions to international palates.
                </p>
                <p>
                  They started experimenting in Maria's tiny kitchen, creating fusion dishes that combined 
                  Mexican spices with Vietnamese herbs and techniques. The result was magical – tacos with 
                  lemongrass chicken, pizzas topped with elote corn, and burritos filled with Vietnamese-style vegetables.
                </p>
                <p>
                  Word spread quickly through the expat and local communities. What started as weekend pop-ups 
                  in friends' homes became a full-fledged restaurant in the heart of Thảo Điền.
                </p>
              </div>
            </motion.div>
            
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              <div className="rounded-3xl overflow-hidden shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1600891964599-f61ba0e24092?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
                  alt="Our Kitchen"
                  className="w-full h-96 object-cover"
                />
              </div>
              <div className="absolute -bottom-6 -left-6 bg-amber-500 text-white p-4 rounded-xl shadow-lg">
                <div className="flex items-center gap-2">
                  <Star className="fill-current" size={20} />
                  <span className="font-semibold">5 Stars</span>
                </div>
                <p className="text-sm">Google Reviews</p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Our Values</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              These core principles guide everything we do at Simple Place.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => {
              const Icon = value.icon
              return (
                <motion.div
                  key={value.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow text-center"
                >
                  <div className="w-16 h-16 bg-amber-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Icon className="text-amber-600" size={32} />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{value.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{value.description}</p>
                </motion.div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Meet Our Team</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              The passionate people behind Simple Place's delicious fusion cuisine.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={member.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="text-center"
              >
                <div className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow">
                  <div className="w-32 h-32 rounded-full overflow-hidden mx-auto mb-4">
                    <img
                      src={member.image}
                      alt={member.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">{member.name}</h3>
                  <p className="text-amber-600 font-medium mb-3">{member.role}</p>
                  <p className="text-gray-600 leading-relaxed">{member.bio}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Location & Hours */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <div className="flex items-center gap-3 mb-6">
                <MapPin className="text-amber-600" size={24} />
                <h3 className="text-2xl font-bold text-gray-900">Visit Us</h3>
              </div>
              <div className="space-y-4">
                <p className="text-gray-600">
                  <strong>Address:</strong><br />
                  199F Nguyễn Văn Hưởng, Thảo Điền<br />
                  Quận 2, Hồ Chí Minh, Vietnam
                </p>
                <p className="text-gray-600">
                  <strong>Phone:</strong> (+84) 904421089<br />
                  <strong>Email:</strong> simpleplace@gmail.com
                </p>
                <p className="text-gray-600">
                  Located in the heart of Thảo Điền, we're easily accessible by 
                  motorbike, car, or Grab. Free parking available on-site.
                </p>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8 }}
              className="bg-white rounded-2xl p-8 shadow-lg"
            >
              <div className="flex items-center gap-3 mb-6">
                <Clock className="text-amber-600" size={24} />
                <h3 className="text-2xl font-bold text-gray-900">Opening Hours</h3>
              </div>
              <div className="space-y-3">
                {[
                  { day: 'Monday - Thursday', hours: '11:00 - 22:00' },
                  { day: 'Friday', hours: '11:00 - 23:00' },
                  { day: 'Saturday', hours: '10:00 - 23:00' },
                  { day: 'Sunday', hours: '10:00 - 21:00' }
                ].map((schedule, index) => (
                  <div key={index} className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="font-medium text-gray-900">{schedule.day}</span>
                    <span className="text-gray-600">{schedule.hours}</span>
                  </div>
                ))}
              </div>
              <div className="mt-6 p-4 bg-amber-50 rounded-xl">
                <p className="text-sm text-amber-800">
                  <strong>Note:</strong> We recommend making reservations for weekends and special occasions. 
                  Walk-ins are always welcome!
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default About
