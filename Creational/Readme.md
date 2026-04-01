Creational Patterns
Factory

Intent: centralize object creation behind a single method — caller asks for a type, factory returns the right object
When to use: when you have multiple subclasses of one type and don't want callers coupled to concrete classes. e.g. VehicleFactory.create("car")

Abstract Factory

Intent: create families of related objects together — guarantees consistency across a product family
When to use: when objects come in groups that must match. e.g. MacButton must never mix with WindowsCheckbox — the factory enforces the family

Singleton

Intent: ensure only one instance of a class exists globally
When to use: shared resources where multiple instances would cause bugs or waste — connection pools, config managers, loggers. Use sparingly — it makes testing harder