# Introduction

One innate feature of evolutionary robotics is the notion of spatial presence - that is the physical world has profound impacts on the emergant behaviors of the agents within. When agents are competing for self-preservation and happen to exchange resources amongst themselves in light of this, an economy is formed. 

This reseach strives to provide an elegant solution to this problem by introducing an algorithm based on fuzzy logic known as the CC (Commerce & Crafting) algorithm.



## The Marketplace

The Marketplace is arguably the most important location on the map. It enables commerce between agents and provides agents with the necasary tools to craft items.

### Commerce

Agents within the Marketplace can partake in commerce with one another. A trading post is available which allows agents to anonymously buy and sell items. Agents need not interact with eachother directly to perform transactions.

### Crafting

Agents within the Marketplace also have access to crafting stations that provide the necesary tools to forge items out of raw materials found in the world.

## Items

Items that exist within the simulation fall into one of two categories.

* Raw materials that are gathered from the world.
* Crafted items produced by combining raw materials. Such items provide agents with attribute bonuses (i.e. movement speed).

## CC Algorithm

The CC (Commerce & Crafting) algorithm utilizes a probability table to determine how an agent will act in the Marketplace.

### Probability Table

* CommitToCraft
* SellUneededGoods
* BuyComponent
* SellComponent
* BuyItem
* SellItem

## Simulation (Change)

### Initialization

Agents in the population each start off with an empty inventory and a fixed amount of coin. Agents are initially located in the Marketplace. The commerce section of the Marketplace starts off with no listings - agents must collect

### Starting the Economy

When the simulation begins, agents venture out of the Marketplace in search of natural resources. When an agent encounters a natural resource, it picks up the resource and heads back to the Marketplace. Upon ariving at the Marketplace the agent always performs the following actions, in order:

* The agent stops by the trading post to partake in commerce. 
	* Any profits from selling items are collected.
	* The agent may browse the trading post and make purchases (buy) or create their own listings (sell).