DEPARTMENT_MENUS = {
    "Training": [        
        {"name": "Settings", "url": "settings", "sub":
        [{"name": "Branches", "url": "branches"},{"name": "Courses", "url": "courses"},{"name": "Batches", "url": "batches"},{"name": "Trainers", "url": "faculty"}]},
        # {"name": "Courses", "url": "courses"},
        # {"name": "Batches", "url": "batches"},
        # {"name": "Trainers", "url": "faculty"},
        {"name": "Reports", "url": "faculty", "sub":
        [{"name": "Review Summary", "url": "all-month-reviews"},{"name": "Monthly Report", "url": "monthly-review-report"}]},
    ],
    "Sales": [        
        {"name": "Settings", "url": "settings", "sub":
        [{"name": "Sales Team", "url": "sales"}]},
        {"name": "Reports", "url": "sales", "sub":
        [{"name": "Review Summary", "url": "sales-all-month-reviews"},{"name": "Monthly Report", "url": "sales-monthly-review-report"}]},
    ],
    "Placement": [
        {"name": "Settings", "url": "settings", "sub":
        [{"name": "Placement Team", "url": "placement"}]},
        {"name": "Reports", "url": "placement", "sub":
        [{"name": "Review Summary", "url": "placement-all-month-reviews"},{"name": "Monthly Report", "url": "placement-monthly-review-report"}]},
    ],
}
