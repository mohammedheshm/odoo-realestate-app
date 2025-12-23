# Odoo Realestate App Module

## Overview
This is a **Real Estate Management System** built as an Odoo module.  
It provides full functionality to manage properties, clients, agents, and transactions efficiently.  

The module demonstrates advanced Odoo development features including models, views, wizards, security, automated actions, RESTful APIs, and unit testing.

---

## Features

### Models & Relationships
- Properly designed **models** with relationships (`Many2one`, `One2many`, `Many2many`)  
- **Sequence fields** for automatic numbering  
- **State fields** for workflow tracking  
- Computed fields with `@api.depends`  
- On-change methods with `@api.onchange` decorators  

### Views & Menus
- Custom **menus** and submenus for easy navigation  
- **Smart buttons** and **Web ribbons** for enhanced UX  
- **Custom buttons** to trigger actions and wizards  
- **State flow** UI for tracking record progress  

### Inheritance & Customization
- Model inheritance (`_inherit`) and XML inheritance for view customization  
- **Update restrictions**: prevent editing of records in certain states  

### Actions & Automations
- **Server actions** for custom logic  
- **Automated actions** for scheduled tasks  

### Reports
- Custom **reports** using QWeb templates  
- Dynamic data rendering for PDF/HTML outputs  

### Wizards
- Wizard interfaces for multi-step operations and task assignments  

### Security & Access
- **Access rights** per model and group  
- Record rules and field-level restrictions  
- **Translation-ready** for multi-language support  

### API
- Full **RESTful JSON API endpoints** (CRUD operations) for properties, clients, and agents  

### Testing
- **Unit tests** included for models, controllers, and workflows  

---

## Installation
1. Place the module in your Odoo `custom_addons` directory  
2. Update `addons_path` in `odoo.conf` to include `custom_addons`  
3. Restart Odoo server  
4. Activate developer mode and install the module from Apps  

---

## API Endpoints
- `GET /v1//api/properties` - List all properties  
- `POST /v1//api/properties` - Create new property  
- `GET /v1//api/properties/<id>` - Get property details  
- `PUT /v1//api/properties/<id>` - Update property  
- `DELETE /v1//api/properties/<id>` - Delete property  

> JSON response format, error handling included
