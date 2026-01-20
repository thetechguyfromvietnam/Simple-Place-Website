'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import menuData from '@/data/menu.json'

interface MenuItem {
  id: number
  name: string
  nameEn: string
  price: number
  unit: string
  category: string
  isBestSeller: boolean
  isVegetarian: boolean
  isSpicy: boolean
  isKidSize: boolean
  image?: string | null
}

export default function Menu() {
  const [activeFilter, setActiveFilter] = useState('Best Sellers')
  const [menuItems, setMenuItems] = useState<MenuItem[]>([])

  useEffect(() => {
    // Load menu items and normalize image field (convert null to undefined)
    const items = (menuData.items || []).map(item => ({
      ...item,
      image: item.image ?? undefined
    }))
    setMenuItems(items)
  }, [])

  const categories = ['Best Sellers', 'All', ...(menuData.categories || [])]

  const filteredItems = activeFilter === 'Best Sellers'
    ? menuItems.filter(item => item.isBestSeller)
    : activeFilter === 'All'
    ? menuItems
    : menuItems.filter(item => item.category === activeFilter)

  const formatPrice = (price: number) => {
    return price.toLocaleString('vi-VN')
  }

  const getImagePath = (item: MenuItem) => {
    // Use image from JSON if available
    if (item.image) {
      return item.image.startsWith('/') ? item.image : `/images/${item.image}`
    }
    return null
  }

  return (
    <section id="menu" className="px-4 md:px-8 lg:px-12 py-16">
      <div className="mx-auto max-w-6xl">
        <div className="mb-6 flex items-end justify-between gap-4" data-aos="fade-up">
          <div>
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tight">Menu</h2>
            <p className="text-neutral-600">Yellow‑hot fusion favorites. Sizes are 10&quot; unless noted.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setActiveFilter(category)}
                className={`filter-btn rounded-xl border px-4 py-2 text-sm transition-colors ${
                  activeFilter === category
                    ? 'bg-amber-500 text-white hover:bg-amber-600'
                    : 'bg-white hover:bg-amber-50'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3">
          {filteredItems.map((item, index) => {
            const imagePath = getImagePath(item)
            return (
              <article
                key={item.id}
                className="menu-card rounded-2xl border bg-white p-5 relative overflow-hidden flex flex-col"
                data-aos="fade-up"
                data-aos-delay={200 + (index % 10) * 50}
              >
                <div className="flex items-center justify-between gap-3 mb-2">
                  <h3 className="text-xl font-semibold flex-1">{item.name}</h3>
                  <span className="price-tag text-base font-medium text-amber-700 bg-amber-100 px-3 py-1 rounded-full whitespace-nowrap">
                    {formatPrice(item.price)} ₫
                  </span>
                </div>
                {item.nameEn && (
                  <p className="text-neutral-600 text-sm mb-3">{item.nameEn}</p>
                )}
                <div className="mb-4 flex items-center justify-between text-xs text-neutral-500">
                  <span>
                    {item.isVegetarian && 'Vegetarian'}
                    {item.isSpicy && 'Spicy'}
                    {item.isKidSize && 'Kid Size'}
                    {!item.isVegetarian && !item.isSpicy && !item.isKidSize && item.category}
                  </span>
                  <span className="inline-flex items-center gap-1">
                    <span className={`inline-block h-2 w-2 rounded-full ${
                      item.isVegetarian ? 'bg-green-500' :
                      item.isSpicy ? 'bg-red-500' :
                      item.isKidSize ? 'bg-yellow-400' :
                      'bg-amber-400'
                    }`}></span>
                    {item.category}
                  </span>
                </div>
                {imagePath && (
                  <div className="mt-auto w-full aspect-[4/3] rounded-xl overflow-hidden relative bg-neutral-100">
                    <Image
                      src={imagePath}
                      alt={item.name}
                      fill
                      className="object-cover rounded-xl"
                      sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                    />
                  </div>
                )}
              </article>
            )
          })}
        </div>

        <div className="mt-8 text-center" data-aos="fade-up" data-aos-delay="800">
          <a
            href="https://www.foodbooking.com/ordering/restaurant/menu?company_uid=0c670ecc-f5f8-48f9-831a-800a7831f98d&restaurant_uid=65f7acf1-fa1e-4a04-98ad-ed4e9f4bbb64&facebook=true"
            target="_blank"
            rel="noopener"
            className="btn-enhanced rounded-2xl px-5 py-3 text-sm font-semibold transition bg-amber-500 text-white hover:bg-amber-600 inline-flex items-center gap-2"
          >
            Order these online →
          </a>
        </div>
      </div>
    </section>
  )
}
