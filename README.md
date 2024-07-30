# My Cook Hub

## Introduction

My Cook Hub is a website for cooking enthusiasts to create and store there home made recipes. The user can also retrieve the recipes from the database to use as and when they please.

Visit the deployed site [here]().

## Table of Contents

1. [User Experience (UX)](#user-experience-ux)
    1. [Project Goals](#project-goals)
    2. [User Stories](#user-stories)
    3. [Color Scheme](#color-scheme)
    4. [Typography](#typography)
    5. [Wireframes](#wireframes)
2. [Features](#features)
    1. [General](#general)
    2. [Landing Page](#landing-page)
    3. [Get Started Page](#get-started-page)
    4. [View Recipes Page](#view-recipes-page)
    5. [My Recipes Page](#my-recipes-page)
    6. [Recipe Page](#recipe-page)
    7. [Create Recipe Page](#create-recipe-page)
    8. [Edit Recipe Page](#edit-recipe-page)
    9. [Create Account Page](#create-account-page)
    10. [Sign In Page](#sign-in-page)
3. [Technologies Used](#technologies-used)
    1. [Languages Used](#languages-used)
    2. [Frameworks, Libraries and Programs Used](#frameworks-libraries-and-programs-used)
4. [Testing](#testing)
    1. [Testing User Stories](#testing-user-stories)
    2. [Code Validation](#code-validation)
    3. [Accessibility](#accessibility)
    4. [Tools Testing](#tools-testing)
    5. [Manual Testing](#manual-testing)
5. [Finished Product](#finished-product)
6. [Deployment](#deployment)
    1. [GitHub Pages](#heroku)
7. [Credits](#credits)
    1. [Content](#content)
    2. [Media](#media)
    3. [Code](#code)
8. [Acknowledgements](#acknowledgements)

***

## User Experience (UX)

## Project Goals

- The application can be easily navigated and understood.
- Clearly explains the concept of the application.
- Clearly explains how to use the application.
- Contains clear imagery and content.
- Provides interactivity in the form of clickable elements.
- Provides feedback when the user performs a specific function.
- Provides users with the ability to create their own profile.
- Provides users with the ability to 'Create' their own recipe.
- Provides users with the ability to access a wide range of recipes and view their full content ('Read').
- Provides users with the ability to edit ('Update') recipes they have created.
- Provides users with the ability to 'Delete' recipes they have created.
- Provides users with the ability to search all recipes depending on keyword.
- Provides users with the ability to save recipes and add them to their 'CookBook'.
- Provides users with the ability to remove recipes from their 'CookBook'.

## User Stories

- As a user, I want to be able to navigate the application easily, so that I can start using the application as soon as possible.
- As a user, I want to know what the application is about, so that I can understand the concept behind it.
- As a user, I want to be able to interact with the application, so that I can have a enjoyable experience.
- As a user, I want to be given feedback when I interact with the application, so I know when an action I perform has been registered.
- As a user, I want to be able to create my own profile, so I can begin using the application to its fullest.
- As a user, I want to be able to add my own recipes, so I can share my knowledge with others.
- As a user, I want to be able to access a wide range of recipes, so that I can find something that I like.
- As a user, I want to be able to edit my own recipes, so that I can make changes to the recipe or fix errors if needed.
- As a user, I want to be able to delete my own recipes, so that I can remove my information if I change my mind.
- As a user, I want to be able to search for a specific recipe, so that I can see which recipes suit my preferences.
- As a user, I want to be able to save recipes to my profile, so that I can view only the recipes that matter to me.
- As a user, I want to be able to remove recipes from my profile, so that I can view only the recipes that matter to me.
- As a user, I want the web application to be responsive, so that I can use the application on a variety of screen sizes.

## Colour Scheme

![My Cook Hub Colour Scheme](src/static/images/Color%20Palette.png)

The primary colours used for this application are as follows:

- Aqua blue (#05A0FA) - Used for the main buttons.

- Dark Grey (#242427) / Black (#121213) - User for the footer background colors.

- Light Grey (#F2F2F2) / White (#FFFFFF) - User for the main background colors.

Additional shades of the primary colors were used on certain elements:

## Typography

- System Ui was used as the main font for the application with sans-serif as a fallback.

## Wireframes

[Figma](https://www.balsamiq.com/) was used to develop the initial concept of the main page of the application - the 'Recipes' page - as well as the Profile page, which follows a similar approach. The developer wanted to keep the main layout of this page a common theme across other pages of the application. However, the ideas for other pages were conceived as the project grew.


| PAGE | DESKTOP WIREFRAME | TABLET WIREFRAME | MOBILE WIREFRAME
| :-- | :-- | :-- | :--
| LANDING PAGE | ![Desktop Landing Page](src/static/images/Desktop%20Landing%20Page%20Wireframe.png) | :-- | :--
| GET STARTED PAGE | ![Desktop Landing Page](src/static/images/Desktop%20Get%20Started%20Page%20Wireframe.png) | :-- | :--
| VIEW RECIPES PAGE | ![View Recipes Page](src/static/images/Desktop%20View%20Recipes%20Wireframe.png) | :-- | :--
| MY RECIPES PAGE | ![My Recipes Page](src/static/images/Desktop%20My%20Recipes%20Wireframe.png) | :-- | :--
| RECIPE PAGE | ![Recipe Page](src/static/images/Desktop%20Recipe%20Page%20Wireframe.png) | ![Recipe Page](src/static/images/Tablet%20Recipe%20Page%20Wireframe.png) | ![Recipe Page](src/static/images/Moblie%20Recipe%20Page%20Wireframe.png)
| CREATE RECIPE PAGE | ![Create Recipe Page](src/static/images/Desktop%20Create%20Recipe%20Wireframe.png) | ![Create Recipe Page](src/static/images/Tablet%20Create%20Recipe%20Wireframe.png) | ![Create Recipe Page](src/static/images/Mobile%20Create%20Recipe%20Wireframe.png)
| EDIT RECIPE PAGE | ![Edit Recipe Page](src/static/images/Desktop%20Edit%20Recipe%20Wireframe.png) | ![Edit Recipe Page](src/static/images/Tablet%20Edit%20Recipe%20Wireframe.png) | ![Edit Recipe Page](src/static/images/Mobile%20Edit%20Recipe%20Wireframe.png)

# Relational vs Non-Relational Database

Relational databases and non-relational databases are two of many databases which can be utilised in a web application. Each database differs in the way it uses data models and how data can be scaled with each model.

1. Relational
   1. Follow a structured, table-based model
   2. Data organised in rows and columns
   3. Good at managing structured data with complex relationships 
   4. Suitable for applications requiring strong consistency, such as financial systems
2. Non-Relational
   1. Flexible data models like documents, key-value pairs, or graphs
   2. Prioritize scalability and accommodate dynamic, unstructured data
   3. Good at delivering horizontal scalability, such as web applications or real-time analytics

# Database Schemas

The database used for this application is stored in the non-relational database __MongoDB__, which is known for using a "schema-less" or "schema-flexible" modeling concept. The reason behind the choice to use a non-relational database for this application was that the relation between each data-model wasn't as complex as - and didn't need to be manipulated like - a relational database data-model.

Please see below for examples of each data-model.

## Account

This schema is used to store details of a user after they have created their account. The keys of this object are used in the following ways:

<details>
<summary>Model</summary>

- `_id`: ObjectId (Automatically generated unique identifier)
- `first_name`: String (User's chosen first name)
- `last_name`: String (User's chosen last name)
- `username`: String (User's chosen username)
- `date_of_birth`: String (User's chosen date of birth)
- `email`: String (User's chosen email address)
- `password`: String (User's password - this is hashed, using Werkzeug's Security Helper 'generate_password_hash')
- `my_recipes`: Array (User's saved recipes - this array is empty upon user-creation)
  - `0`: String (ObjectID of recipe)
  - `1`: String (ObjectID of recipe)
  - `2`: String (ObjectID of recipe)

</details>

<details>
<summary>Example</summary>

```json
{
  "_id": ObjectId("659153d1b9ce951d2bdf6597"),
  "first_name": "Bill",
  "last_name": "Plant",
  "username": "exampleuser123",
  "date_of_birth": "11/11/1970",
  "email": "exampleuser@123.com",
  "password": "scrypt:32768:8:1$ZbOMTxq9TMnRiLev$3...",
  "my_recipes": {
    0: "6591544fb9ce951d2bdf6598",
    1: "6591545bdd6d1822d9e9d4c3",
    2: "65915467dd6d1822d9e9d4c4"
  }
}
```
</details>

## Recipe

