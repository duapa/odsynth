# Core Idea

At the core of this project lies the concept that every dataset can be viewed as a hierarchy of records, where each record may contain multiple fields. This concept is particularly evident in hierarchical datasets such as JSON and XML. For instance, in JSON, each object can contain nested objects or arrays, illustrating this hierarchical structure. On the other hand, tabular data, like CSV files, can be conceptualized with the table itself as a root record. Each field within the table then stands as an individual member of the record.

We can therefore implement a system for creating an object model out of dataset's schema by building such a hierarchy of data elements. We can further build validators for object models and use the valid object models to generate data according to any schema of our choosing. The Composite Pattern is a software pattern that facilitates the definition of hierarchies of objects and is useful in defining the core structures of this solution.

Based on the Composite Pattern, the following are defined:
1. [Record](../odsynth/core/object_model.py): Implements a Composite object and defines a root of the object model or field which contains sub fields
1. [Field](../odsynth/core/object_model.py): Implements a Leaf object and defines a primitive field that contains atomic data(int, float, string, bool, etc)

## On Providers
Providers are sub types of the Field class and implement the generation of atomic data. [Faker](https://github.com/joke2k/faker) inspires this project and is used to create the generators of atomic data. Currently we have developed a few Providers to seed the project:
* FirstName
* LastName
* RandomInt
* SSN
* Text

We hope to add more providers as time goes on.
