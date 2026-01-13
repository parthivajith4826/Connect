[1mdiff --git a/freelancer/urls.py b/freelancer/urls.py[m
[1mindex a6a013d..a3e1ac6 100644[m
[1m--- a/freelancer/urls.py[m
[1m+++ b/freelancer/urls.py[m
[36m@@ -18,6 +18,7 @@[m [murlpatterns = [[m
     [m
     [m
     path('find-work',views.find_work,name = 'find_work'),[m
[32m+[m[32m    path('work-details/<slug:slug>',views.card_details,name = 'work_details')[m
     [m
     [m
 [m
[1mdiff --git a/freelancer/views.py b/freelancer/views.py[m
[1mindex 9db4f55..f4a4f29 100644[m
[1m--- a/freelancer/views.py[m
[1m+++ b/freelancer/views.py[m
[36m@@ -509,6 +509,45 @@[m [mdef subscription_success(request):[m
     return render(request,"freelancer/subscription_success.html")[m
 [m
 [m
[31m-[m
[32m+[m[32mfrom client.models import Card,Categories[m
 def find_work(request):[m
[31m-    return render(request,"freelancer/find_work.html")[m
\ No newline at end of file[m
[32m+[m[32m    print(request.GET)[m
[32m+[m[32m    categories = Categories.objects.all()[m
[32m+[m[32m    search_keyword = request.GET.get("q")[m
[32m+[m[32m    category = request.GET.get("category")[m
[32m+[m[32m    skills = request.GET.get("skills")[m
[32m+[m[32m    minimum_price = request.GET.get("min_price")[m
[32m+[m[32m    maximum_price = request.GET.get("max_price")[m
[32m+[m[32m    timeline = request.GET.get("timeline")[m
[32m+[m[41m    [m
[32m+[m[41m    [m
[32m+[m[32m    cards = Card.objects.none()[m
[32m+[m[32m    if search_keyword :[m
[32m+[m[32m        cards = Card.objects.filter(title__icontains = search_keyword, is_blocked = False )[m
[32m+[m[32m        # cards = cards.filter(is_active = )[m
[32m+[m[32m    if category :[m
[32m+[m[32m        cards = cards.filter(category_id = category )[m
[32m+[m[32m    if skills :[m
[32m+[m[32m        cards = cards.filter(skills_required__icontains = skills)[m
[32m+[m[41m    [m
[32m+[m[32m    if minimum_price is not None and maximum_price is not None:[m
[32m+[m[32m        cards = cards.filter([m
[32m+[m[32m            min_budget__gte = minimum_price,[m
[32m+[m[32m            max_budget__lte=maximum_price[m
[32m+[m[32m        )[m
[32m+[m[41m    [m
[32m+[m[32m    if timeline :[m
[32m+[m[32m        cards = cards.filter(time_line__icontains = timeline)[m
[32m+[m[41m        [m
[32m+[m[32m    if request.GET.get("newest"):[m
[32m+[m[32m        cards = cards.order_by("-created_at")[m
[32m+[m
[32m+[m
[32m+[m[32m    return render(request,"freelancer/find_work.html",{"cards":cards,"categories":categories})[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m[32mdef card_details(request,slug):[m
[32m+[m[32m    card = get_object_or_404(Card,slug = slug)[m
[32m+[m[32m    skill_list = card.skills_required.split(",")[m
[32m+[m[32m    return render(request,"freelancer\card_details.html",{"card":card,"skill_list":skill_list})[m
\ No newline at end of file[m
[1mdiff --git a/templates/client/create_card.html b/templates/client/create_card.html[m
[1mindex c94df9e..b98bd67 100644[m
[1m--- a/templates/client/create_card.html[m
[1m+++ b/templates/client/create_card.html[m
[36m@@ -177,7 +177,7 @@[m
 [m
                         <!-- Hidden input sent to Django -->[m
                         <input type="hidden" name="description" id="description" />[m
[31m-                        {{ form.description.errors }}[m
[32m+[m[32m                    {{ form.description.errors }}[m
                     </div>[m
                 [m
 [m
[1mdiff --git a/templates/freelancer/find_work.html b/templates/freelancer/find_work.html[m
[1mindex 411960b..8ddc585 100644[m
[1m--- a/templates/freelancer/find_work.html[m
[1m+++ b/templates/freelancer/find_work.html[m
[36m@@ -42,15 +42,15 @@[m
         animation-delay: 0.3s;[m
     }[m
 </style>[m
[32m+[m
 <!-- Main Content Area -->[m
[31m-<main class="flex-1 overflow-y-auto h-screen bg-[#f5f5f7]">[m
[31m-    <!-- Top Header with Search and Filters -->[m
[32m+[m[32m<main class="flex-1 overflow-y-auto h-screen bg-[#f5f5f7] flex flex-col">[m
[32m+[m[32m    <!-- Top Header with Search -->[m
     <header class="bg-white border-b border-gray-200 sticky top-0 z-20">[m
[31m-        <!-- Search Bar Row -->[m
         <div class="px-8 py-4 flex items-center justify-between">[m
             <h1 class="text-xl font-bold text-[#1d1d1f]">Find Work</h1>[m
             <div class="flex-1 max-w-2xl mx-8 relative">[m
[31m-                <div class="relative group">[m
[32m+[m[32m                <form id="searchForm" class="relative group" method="GET" action="">[m
                     <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">[m
                         <svg[m
                             class="h-5 w-5 text-gray-400 group-focus-within:text-[#0071e3] transition-colors"[m
[36m@@ -67,12 +67,20 @@[m
                         </svg>[m
                     </div>[m
                     <input[m
[32m+[m[32m                        id="searchInput"[m
                         type="text"[m
[32m+[m[32m                        name="q"[m
                         class="block w-full pl-11 pr-4 py-3 bg-gray-50 border border-transparent rounded-full text-sm placeholder-gray-500 focus:bg-white focus:border-[#0071e3] focus:ring-1 focus:ring-[#0071e3] focus:outline-none transition-all shadow-sm"[m
                         placeholder="Search by category, skill, or keyword..."[m
[32m+[m[32m                        autocomplete="off"[m
[32m+[m[32m                        value="{{ request.GET.q|default:'' }}"[m
                     />[m
                     <div class="absolute inset-y-0 right-0 pr-3 flex items-center">[m
[31m-                        <button class="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100">[m
[32m+[m[32m                        <button[m
[32m+[m[32m                            type="button"[m
[32m+[m[32m                            id="clearSearch"[m
[32m+[m[32m                            class="p-1 text-gray-400 hover:text-gray-600 rounded-full hover:bg-gray-100 hidden"[m
[32m+[m[32m                        >[m
                             <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">[m
                                 <path[m
                                     stroke-linecap="round"[m
[36m@@ -83,82 +91,236 @@[m
                             </svg>[m
                         </button>[m
                     </div>[m
[31m-                </div>[m
[32m+[m[32m                </form>[m
             </div>[m
             <div class="w-20"></div>[m
[31m-            <!-- Spacer balance -->[m
         </div>[m
 [m
[31m-        <!-- Filters Row -->[m
[31m-        <div class="px-8 pb-4 flex items-center gap-3 overflow-x-auto no-scrollbar">[m
[32m+[m[32m        <!-- Filters Row (Hidden Initially) -->[m
[32m+[m[32m        <form id="filterRow" class="hidden px-8 pb-4 items-center gap-3 overflow-visible animate-fade-in-up" method="GET">[m
[32m+[m[32m            <input type="hidden" name="q" value="{{ request.GET.q }}" />[m
[32m+[m
             <!-- Category Filter -->[m
[31m-            <div class="relative group">[m
[32m+[m[32m            <div class="relative group" id="categoryFilter">[m
                 <button[m
[31m-                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-[#0071e3] hover:text-[#0071e3] transition-colors"[m
[32m+[m[32m                    type="button"[m
[32m+[m[32m                    onclick="toggleDropdown('categoryDropdown')"[m
[32m+[m[32m                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded hover:border-[#0071e3] transition-colors text-sm font-semibold text-gray-700"[m
                 >[m
                     Category[m
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">[m
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>[m
                     </svg>[m
                 </button>[m
[32m+[m[32m                <div[m
[32m+[m[32m                    id="categoryDropdown"[m
[32m+[m[32m                    class="hidden absolute top-full left-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-100 p-4 z-50"[m
[32m+[m[32m                >[m
[32m+[m[32m                    <div class="space-y-2 max-h-60 overflow-y-auto custom-scrollbar">[m
[32m+[m[32m                        {% for category in categories %}[m
[32m+[m[32m                        <label class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded cursor-pointer">[m
[32m+[m[32m                            <input[m
[32m+[m[32m                                type="checkbox"[m
[32m+[m[32m                                name="category"[m
[32m+[m[32m                                value="{{ category.id }}"[m
[32m+[m[32m                                class="w-4 h-4 text-[#0071e3] rounded border-gray-300 focus:ring-[#0071e3]"[m
[32m+[m[32m                            />[m
[32m+[m[32m                            <span class="text-sm text-gray-700">{{ category.name }}</span>[m
[32m+[m[32m                        </label>[m
[32m+[m[32m                        {% endfor %}[m
[32m+[m[32m                    </div>[m
[32m+[m[32m                    <div class="pt-3 mt-2 border-t border-gray-100 flex justify-end">[m
[32m+[m[32m                        <button type="submit" class="text-sm font-bold text-[#0071e3] hover:underline">Apply</button>[m
[32m+[m[32m                    </div>[m
[32m+[m[32m                </div>[m
             </div>[m
 [m
[31m-            <!-- Skills Filter -->[m
[32m+[m[32m            <!-- Skills Filter (Mini Search Bar) -->[m
             <div class="relative group">[m
[31m-                <button[m
[31m-                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-[#0071e3] hover:text-[#0071e3] transition-colors"[m
[31m-                >[m
[31m-                    Skills[m
[31m-                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">[m
[31m-                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>[m
[31m-                    </svg>[m
[31m-                </button>[m
[32m+[m[32m                <input[m
[32m+[m[32m                    type="text"[m
[32m+[m[32m                    name="skills"[m
[32m+[m[32m                    placeholder="Search skills..."[m
[32m+[m[32m                    class="px-4 py-2 bg-white border border-gray-300 rounded text-sm text-gray-700 placeholder-gray-500 focus:border-[#0071e3] focus:ring-1 focus:ring-[#0071e3] outline-none w-48 transition-all"[m
[32m+[m[32m                />[m
             </div>[m
 [m
[31m-            <!-- Budget Filter -->[m
[31m-            <div class="relative group">[m
[32m+[m[32m            <!-- Price Filter -->[m
[32m+[m[32m            <div class="relative group" id="priceFilter">[m
                 <button[m
[31m-                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-[#0071e3] hover:text-[#0071e3] transition-colors"[m
[32m+[m[32m                    type="button"[m
[32m+[m[32m                    onclick="toggleDropdown('priceDropdown')"[m
[32m+[m[32m                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded hover:border-[#0071e3] transition-colors text-sm font-semibold text-gray-700"[m
                 >[m
                     Price[m
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">[m
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>[m
                     </svg>[m
                 </button>[m
[32m+[m[32m                <div[m
[32m+[m[32m                    id="priceDropdown"[m
[32m+[m[32m                    class="hidden absolute top-full left-0 mt-2 w-80 bg-white rounded-lg shadow-xl border border-gray-100 p-6 z-50"[m
[32m+[m[32m                >[m
[32m+[m[32m                    <div class="flex items-center justify-between mb-6">[m
[32m+[m[32m                        <div class="border rounded px-3 py-1">[m
[32m+[m[32m                            <span class="text-xs text-gray-500 block">MIN</span>[m
[32m+[m[32m                            <div class="flex items-center">[m
[32m+[m[32m                                <span class="text-sm text-gray-700">₹</span>[m
[32m+[m[32m                                <input[m
[32m+[m[32m                                    type="number"[m
[32m+[m[32m                                    name="min_price"[m
[32m+[m[32m                                    value="0"[m
[32m+[m[32m                                    class="w-16 text-sm outline-none font-bold"[m
[32m+[m[32m                                    min="0"[m
[32m+[m[32m                                    max="500000"[m
[32m+[m[32m                                />[m
[32m+[m[32m                            </div>[m
[32m+[m[32m                        </div>[m
[32m+[m[32m                        <span class="text-gray-300">-</span>[m
[32m+[m[32m                        <div class="border rounded px-3 py-1">[m
[32m+[m[32m                            <span class="text-xs text-gray-500 block">MAX</span>[m
[32m+[m[32m                            <div class="flex items-center">[m
[32m+[m[32m                                <span class="text-sm text-gray-700">₹</span>[m
[32m+[m[32m                                <input[m
[32m+[m[32m                                    type="number"[m
[32m+[m[32m                                    name="max_price"[m
[32m+[m[32m                                    id="maxPriceInput"[m
[32m+[m[32m                                    value="500000"[m
[32m+[m[32m                                    class="w-16 text-sm outline-none font-bold"[m
[32m+[m[32m                                    min="0"[m
[32m+[m[32m                                    max="500000"[m
[32m+[m[32m                                />[m
[32m+[m[32m                            </div>[m
[32m+[m[32m                        </div>[m
[32m+[m[32m                    </div>[m
[32m+[m[32m                    <!-- Visual Slider with Buttons -->[m
[32m+[m[32m                    <div class="flex items-center gap-4 mb-4">[m
[32m+[m[32m                        <button[m
[32m+[m[32m                            type="button"[m
[32m+[m[32m                            onclick="adjustPrice(-1000)"[m
[32m+[m[32m                            class="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-gray-500 hover:bg-gray-50 text-xl font-bold"[m
[32m+[m[32m                        >[m
[32m+[m[32m                            -[m
[32m+[m[32m                        </button>[m
[32m+[m[32m                        <div class="flex-1 h-2 bg-gray-100 rounded-full relative">[m
[32m+[m[32m                            <!-- Visual Bar -->[m
[32m+[m[32m                            <div[m
[32m+[m[32m                                id="priceBar"[m
[32m+[m[32m                                class="absolute left-0 top-0 h-full bg-[#0071e3] rounded-full"[m
[32m+[m[32m                                style="width: 10%"[m
[32m+[m[32m                            ></div>[m
[32m+[m[32m                            <!-- Invisible Range Input for Dragging -->[m
[32m+[m[32m                            <input[m
[32m+[m[32m                                type="range"[m
[32m+[m[32m                                id="priceRange"[m
[32m+[m[32m                                min="0"[m
[32m+[m[32m                                max="500000"[m
[32m+[m[32m                                step="1000"[m
[32m+[m[32m                                value="50000"[m
[32m+[m[32m                                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"[m
[32m+[m[32m                            />[m
[32m+[m[32m                        </div>[m
[32m+[m[32m                        <button[m
[32m+[m[32m                            type="button"[m
[32m+[m[32m                            onclick="adjustPrice(1000)"[m
[32m+[m[32m                            class="w-8 h-8 rounded-full border border-gray-300 flex items-center justify-center text-gray-500 hover:bg-gray-50 text-xl font-bold"[m
[32m+[m[32m                        >[m
[32m+[m[32m                            +[m
[32m+[m[32m                        </button>[m
[32m+[m[32m                    </div>[m
[32m+[m[32m                    <div class="pt-3 border-t border-gray-100 flex justify-end">[m
[32m+[m[32m                        <button type="submit" class="text-sm font-bold text-[#0071e3] hover:underline">Apply</button>[m
[32m+[m[32m                    </div>[m
[32m+[m[32m                </div>[m
             </div>[m
 [m
             <!-- Timeline Filter -->[m
[31m-            <div class="relative group">[m
[32m+[m[32m            <div class="relative group" id="timelineFilter">[m
                 <button[m
[31m-                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-full text-sm font-medium text-gray-700 hover:border-[#0071e3] hover:text-[#0071e3] transition-colors"[m
[32m+[m[32m                    type="button"[m
[32m+[m[32m                    onclick="toggleDropdown('timelineDropdown')"[m
[32m+[m[32m                    class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded hover:border-[#0071e3] transition-colors text-sm font-semibold text-gray-700"[m
                 >[m
                     Timeline[m
                     <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">[m
                         <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>[m
                     </svg>[m
                 </button>[m
[32m+[m[32m                <div[m
[32m+[m[32m                    id="timelineDropdown"[m
[32m+[m[32m                    class="hidden absolute top-full left-0 mt-2 w-64 bg-white rounded-lg shadow-xl border border-gray-100 p-4 z-50"[m
[32m+[m[32m                >[m
[32m+[m[32m                    <div class="space-y-2">[m
[32m+[m
[32m+[m[32m                        <label class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded cursor-pointer">[m
[32m+[m[32m                            <input[m
[32m+[m[32m                                type="radio"[m
[32m+[m[32m                                name="timeline"[m
[32m+[m[32m                                value="Less than 1 week"[m
[32m+[m[32m                                {% if request.GET.timeline == "Less than 1 week" %}checked{% endif %}[m
[32m+[m[32m                                class="w-4 h-4 text-[#0071e3] border-gray-300 focus:ring-[#0071e3]"[m
[32m+[m[32m                            />[m
[32m+[m[32m                            <span class="text-sm text-gray-700">Less than 1 week</span>[m
[32m+[m[32m                        </label>[m
[32m+[m
[32m+[m[32m                        <label class="flex items-center gap-3 p-2 hover:bg-gray-50 rounded cursor-pointer">[m
[32m+[m[32m                            <input[m
[32m+[m[32m                                type="radio"[m
[32m+[m[32m                                name="timeline"[m
[32m+[m[32m                                value="1 to 4 weeks"[m
[32m+[m[32m                                {% if request.GET.timeline == "1 to 4 weeks" %}checked{% endif %}[m
[32m+[m[32m                                class="w-4 h-4 text-[#0071e3] bo