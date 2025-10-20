import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Search, Filter, ShoppingCart, Star, Phone, Plus } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'
import PizzaSizeSelector from '../components/PizzaSizeSelector'
import TacoOptionsSelector from '../components/TacoOptionsSelector'

const Menu = () => {
  const [menuData, setMenuData] = useState({})
  const [filteredItems, setFilteredItems] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)
  const [showPizzaSizeSelector, setShowPizzaSizeSelector] = useState(false)
  const [showTacoOptionsSelector, setShowTacoOptionsSelector] = useState(false)
  const [selectedPizzaItem, setSelectedPizzaItem] = useState(null)
  const [selectedTacoItem, setSelectedTacoItem] = useState(null)
  const { addToCart, getTotalItems } = useCart()


  // Function to handle pizza size selection and taco options
  const handleAddToCart = (item) => {
    const isPizza = item.isPizza || item.name.toLowerCase().includes('pizza') || item.name.toLowerCase().includes('pizzadilla')
    const isTaco = item.isTaco || item.name.toLowerCase().includes('taco')
    
    if (isPizza) {
      setSelectedPizzaItem(item)
      setShowPizzaSizeSelector(true)
    } else if (isTaco) {
      setSelectedTacoItem(item)
      setShowTacoOptionsSelector(true)
    } else {
      addToCart(item)
    }
  }

  const handlePizzaAddToCart = (pizzaItem) => {
    addToCart(pizzaItem)
  }

  const handleTacoAddToCart = (tacoItem) => {
    addToCart(tacoItem)
  }

  useEffect(() => {
    // Load menu data from the JSON file
    fetch('/menu_data.json')
      .then(response => response.json())
      .then(data => {
        setMenuData(data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error loading menu data:', error)
        setLoading(false)
      })
  }, [])

  useEffect(() => {
    let items = []
    
    if (selectedCategory === 'All') {
      Object.values(menuData).forEach(categoryItems => {
        items.push(...categoryItems)
      })
    } else if (menuData[selectedCategory]) {
      items = menuData[selectedCategory]
    }

    if (searchTerm) {
      items = items.filter(item => 
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    setFilteredItems(items)
  }, [menuData, selectedCategory, searchTerm])

  const categories = ['All', 'Appetizers', 'Salad', 'Tacos', 'Burrito', 'Quesadilla', 'Pizza', 'Spaghetti', 'Main Dish', 'Drinks', 'Extra']
  
  const formatPrice = (price) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price)
  }

  const getItemImage = (item) => {
    // Simple image mapping based on item name
    const name = item.name.toLowerCase()
    if (name.includes('pizza') || name.includes('margherita')) {
      return 'https://images.unsplash.com/photo-1601924572345-0050bd436b0b?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('taco')) {
      return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('burrito')) {
      return 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('quesadilla')) {
      return 'https://images.unsplash.com/photo-1571068316344-75bc76f77890?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('salad')) {
      return 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('soup')) {
      return 'https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('beer') || name.includes('bia')) {
      return 'https://images.unsplash.com/photo-1608270586620-248524c67de9?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('dessert') || name.includes('panna cotta')) {
      return 'https://images.unsplash.com/photo-1551024506-0bccd828d307?q=80&w=400&auto=format&fit=crop'
    } else if (name.includes('spaghetti') || name.includes('penne') || name.includes('lasagna') || name.includes('linguine') || name.includes('fettuccine')) {
      return 'https://images.unsplash.com/photo-1621996346565-e3dbc353d2e5?q=80&w=400&auto=format&fit=crop'
    } else {
      return 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?q=80&w=400&auto=format&fit=crop'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-amber-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading menu...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Our Menu</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Discover our fusion of Mexican and Vietnamese flavors. From authentic tacos to creative pizzas, 
            we bring you the best of both worlds.
          </p>
        </motion.div>

        {/* Search and Filter */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <div className="flex flex-col md:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Search menu items..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all"
                />
              </div>

              {/* Category Filter */}
              <div className="flex items-center gap-2">
                <Filter className="text-gray-400" size={20} />
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-amber-500 focus:border-transparent transition-all bg-white"
                >
                  {categories.map(category => (
                    <option key={category} value={category}>
                      {category}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Category Tabs */}
            <div className="flex flex-wrap gap-2 mt-4">
              {categories.map(category => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-xl text-sm font-medium transition-all ${
                    selectedCategory === category
                      ? 'bg-amber-500 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-amber-100'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Menu Items Grid */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
        >
          {filteredItems.map((item, index) => (
            <motion.div
              key={`${item.name}-${index}`}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="menu-card bg-white rounded-2xl border p-5 relative overflow-hidden shadow-lg hover:shadow-xl"
            >
              {/* Item Image */}
              <div className="h-48 rounded-xl overflow-hidden mb-4">
                <img
                  src={getItemImage(item)}
                  alt={item.name}
                  className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
                />
              </div>

              {/* Item Info */}
              <div className="flex items-start justify-between gap-3 mb-3">
                <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                  {item.name}
                </h3>
                <div className="text-right">
                  <span className="price-tag text-base font-medium text-amber-700 bg-amber-100 px-3 py-1 rounded-full whitespace-nowrap">
                    {formatPrice(item.price)}
                  </span>
                  {item.isPizza && (
                    <div className="text-xs text-gray-600 mt-1">Medium size</div>
                  )}
                  {item.isTaco && (
                    <div className="text-xs text-gray-600 mt-1">Crispy/Soft options</div>
                  )}
                </div>
              </div>

              {/* Item Details */}
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span className="inline-flex items-center gap-1">
                  <Star size={14} className="text-amber-400 fill-current" />
                  Popular
                </span>
                <span className="text-xs bg-gray-100 px-2 py-1 rounded-full">
                  {item.unit}
                </span>
              </div>

              {/* Add to Cart Button */}
                <button 
                  onClick={() => handleAddToCart(item)}
                  className="w-full bg-amber-500 text-white py-3 rounded-xl font-semibold hover:bg-amber-600 transition-all duration-300 flex items-center justify-center gap-2"
                >
                  <Plus size={18} />
                  Add to Cart
                </button>
            </motion.div>
          ))}
        </motion.div>

        {/* No Results */}
        {filteredItems.length === 0 && !loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-12"
          >
            <div className="text-gray-400 mb-4">
              <Search size={48} className="mx-auto" />
            </div>
            <h3 className="text-xl font-semibold text-gray-700 mb-2">No items found</h3>
            <p className="text-gray-500">
              Try adjusting your search or filter to find what you're looking for.
            </p>
          </motion.div>
        )}

        {/* Order Online CTA */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-12 text-center"
        >
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Ready to Order?</h2>
            <p className="text-gray-600 mb-6">
              Order online for pickup or delivery. Fast, fresh, and delicious!
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center">
              <Link
                to="/cart"
                className="btn-enhanced bg-amber-500 text-white px-6 sm:px-8 py-3 rounded-xl font-semibold hover:bg-amber-600 transition-all duration-300 inline-flex items-center justify-center gap-2 text-sm sm:text-base"
              >
                <ShoppingCart size={18} className="sm:w-5 sm:h-5" />
                <span className="hidden xs:inline">View Cart</span>
                <span className="xs:hidden">Cart</span>
                ({getTotalItems()})
              </Link>
              <Link
                to="/booking"
                className="btn-enhanced border-2 border-amber-500 text-amber-700 px-6 sm:px-8 py-3 rounded-xl font-semibold hover:bg-amber-50 transition-all duration-300 inline-flex items-center justify-center gap-2 text-sm sm:text-base"
              >
                📅 <span className="hidden sm:inline">Book a Table</span><span className="sm:hidden">Book</span>
              </Link>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Pizza Size Selector Modal */}
      {showPizzaSizeSelector && selectedPizzaItem && (
        <PizzaSizeSelector
          item={selectedPizzaItem}
          onAddToCart={handlePizzaAddToCart}
          onClose={() => {
            setShowPizzaSizeSelector(false)
            setSelectedPizzaItem(null)
          }}
        />
      )}

      {/* Taco Options Selector Modal */}
      {showTacoOptionsSelector && selectedTacoItem && (
        <TacoOptionsSelector
          item={selectedTacoItem}
          onAddToCart={handleTacoAddToCart}
          onClose={() => {
            setShowTacoOptionsSelector(false)
            setSelectedTacoItem(null)
          }}
        />
      )}
    </div>
  )
}

export default Menu
