fetch('http://127.0.0.1:5000/get_items')
	.then((res) => res.json())
	.then((items) => {
		items.forEach((item) => {
			document
				.querySelector('main')
				.appendChild(
					createItemCard(
						item.name,
						item.description,
						item.rating,
						formatDate(new Date(item.delivery_time)),
						item.price,
						'./assets/ext_item_image.png'
					)
				)
		})

		chrome.storage.local.get(['sortingMethod'], (result) => {
			if (result.sortingMethod) {
				sortItems(result.sortingMethod[0], result.sortingMethod[1])
			}
		})
	})

function sortItems(option, type = 'asc') {
	const elementsToSort = Array.from(document.querySelector('main').children)
	document.querySelector('main').innerHTML = ''

	if (type === 'asc') {
		if (option === 'price') {
			elementsToSort
				.sort(
					(a, b) =>
						+a.children[1].children[1].children[1].children[0].children[0]
							.innerHTML -
						+b.children[1].children[1].children[1].children[0].children[0]
							.innerHTML
				)
				.forEach((element) =>
					document.querySelector('main').appendChild(element)
				)
		}
	} else if (type === 'desc') {
		if (option === 'price') {
			elementsToSort
				.sort(
					(a, b) =>
						+b.children[1].children[1].children[1].children[0].children[0]
							.innerHTML -
						+a.children[1].children[1].children[1].children[0].children[0]
							.innerHTML
				)
				.forEach((element) =>
					document.querySelector('main').appendChild(element)
				)
		} else if (option === 'rating') {
			elementsToSort
				.sort(
					(a, b) =>
						+b.children[1].children[1].children[0].children[0].children[1]
							.innerHTML -
						+a.children[1].children[1].children[0].children[0].children[1]
							.innerHTML
				)
				.forEach((element) =>
					document.querySelector('main').appendChild(element)
				)
		}
	}

	chrome.storage.local.set({ sortingMethod: [option, type] })
}

function formatDate(date) {
	const today = new Date()
	const tomorrow = new Date(today)
	tomorrow.setDate(today.getDate() + 1)

	today.setHours(0, 0, 0, 0)
	tomorrow.setHours(0, 0, 0, 0)
	date.setHours(0, 0, 0, 0)

	if (date.getTime() === today.getTime()) {
		return 'Сегодня'
	} else if (date.getTime() === tomorrow.getTime()) {
		return 'Завтра'
	} else {
		return date.toLocaleDateString('RU-ru', {
			day: 'numeric',
			month: 'short',
			year: 'numeric',
		})
	}
}

function createItemCard(
	name,
	description,
	rating,
	deliveryTime,
	price,
	imageSrc
) {
	// Create the wrapper div
	const itemWrapper = document.createElement('div')
	itemWrapper.className = 'item-wrapper'

	// Create the image wrapper
	const itemImageWrapper = document.createElement('div')
	itemImageWrapper.className = 'item-image-wrapper'

	const itemImage = document.createElement('img')
	itemImage.src = imageSrc
	itemImage.alt = 'Item image'
	itemImageWrapper.appendChild(itemImage)

	// Create the content wrapper
	const itemContentWrapper = document.createElement('div')
	itemContentWrapper.className = 'item-content-wrapper'

	// Create the name and description wrapper
	const nameDescriptionWrapper = document.createElement('div')

	const itemName = document.createElement('p')
	itemName.className = 'item-name'
	itemName.textContent = name

	const itemDescription = document.createElement('p')
	itemDescription.className = 'item-description'
	itemDescription.textContent = description

	nameDescriptionWrapper.appendChild(itemName)
	nameDescriptionWrapper.appendChild(itemDescription)

	// Create the info wrapper
	const itemInfoWrapper = document.createElement('div')
	itemInfoWrapper.className = 'item-info-wrapper'

	// Create rating and delivery time wrapper
	const itemRatingDeliveryTimeWrapper = document.createElement('div')
	itemRatingDeliveryTimeWrapper.className = 'item-rating-delivery-time-wrapper'

	const itemRatingWrapper = document.createElement('div')
	itemRatingWrapper.className = 'item-rating-wrapper'

	const itemRatingImage = document.createElement('span')
	itemRatingImage.className = 'item-rating__image'
	itemRatingImage.innerHTML = `
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
                d="M6 0L7.34708 4.1459H11.7063L8.17963 6.7082L9.52671 10.8541L6 8.2918L2.47329 10.8541L3.82037 6.7082L0.293661 4.1459H4.65292L6 0Z"
                stroke="#8E246C" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
    `

	const itemRatingNumber = document.createElement('span')
	itemRatingNumber.className = 'item-rating__number'
	itemRatingNumber.textContent = rating

	itemRatingWrapper.appendChild(itemRatingImage)
	itemRatingWrapper.appendChild(itemRatingNumber)

	const itemDeliveryTimeWrapper = document.createElement('div')
	itemDeliveryTimeWrapper.className = 'item-delivery-time-wrapper'

	const itemDeliveryTimeImage = document.createElement('span')
	itemDeliveryTimeImage.className = 'item-delivery-time__image'
	itemDeliveryTimeImage.innerHTML = `
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none"
            xmlns="http://www.w3.org/2000/svg">
            <path
                d="M6 3.22222V6L7.38889 5.16667M11 6C11 8.76144 8.76144 11 6 11C3.23858 11 1 8.76144 1 6C1 3.23858 3.23858 1 6 1C8.76144 1 11 3.23858 11 6Z"
                stroke="#8E246C" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
    `

	const itemDeliveryTimeDate = document.createElement('span')
	itemDeliveryTimeDate.className = 'item-delivery-time__date'
	itemDeliveryTimeDate.textContent = deliveryTime

	itemDeliveryTimeWrapper.appendChild(itemDeliveryTimeImage)
	itemDeliveryTimeWrapper.appendChild(itemDeliveryTimeDate)

	itemRatingDeliveryTimeWrapper.appendChild(itemRatingWrapper)
	itemRatingDeliveryTimeWrapper.appendChild(itemDeliveryTimeWrapper)

	// Create the price and button wrapper
	const itemPriceWrapper = document.createElement('div')
	itemPriceWrapper.className = 'item-price-wrapper'

	const itemPrice = document.createElement('p')
	itemPrice.className = 'item-price'
	itemPrice.innerHTML = `<span class='item-price__number'>${price}</span> р`

	const itemButton = document.createElement('button')
	itemButton.type = 'button'
	itemButton.className = 'button-secondary'
	itemButton.textContent = 'купить'

	itemPriceWrapper.appendChild(itemPrice)
	itemPriceWrapper.appendChild(itemButton)

	// Append all inner wrappers to the info wrapper
	itemInfoWrapper.appendChild(itemRatingDeliveryTimeWrapper)
	itemInfoWrapper.appendChild(itemPriceWrapper)

	// Append name, description, and info to the content wrapper
	itemContentWrapper.appendChild(nameDescriptionWrapper)
	itemContentWrapper.appendChild(itemInfoWrapper)

	// Append image and content to the main wrapper
	itemWrapper.appendChild(itemImageWrapper)
	itemWrapper.appendChild(itemContentWrapper)

	return itemWrapper
}

document
	.querySelector('.dropdown-item.dropdown-item__price-desc')
	.addEventListener('click', () => {
		sortItems('price', 'desc')
	})
document
	.querySelector('.dropdown-item.dropdown-item__price-asc')
	.addEventListener('click', () => {
		sortItems('price', 'asc')
	})
document
	.querySelector('.dropdown-item.dropdown-item__rating-desc')
	.addEventListener('click', () => {
		sortItems('rating', 'desc')
	})
document
	.querySelector('.dropdown-item.dropdown-item__delivery-time-asc')
	.addEventListener('click', () => {
		sortItems('deliveryTime', 'asc')
	})
