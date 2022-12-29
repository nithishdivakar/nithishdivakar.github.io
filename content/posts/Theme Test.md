---
title : Theme test
tags: [tag1, tag2]
date: 1991-10-13T00:35:00+05:30
draft: true
---

# Heading1
## Heading2
### Heading3
#### Heading4
##### Heading5

#tags #tags and more #tags

**ncididunt ut labore et dolore magna aliqua.** Ut enim ad ~~minim veniam, quis nostrud exercitation ullamco laboris~~ nisi ut *aliquip ex ea commodo consequat.* Duis aute ==irure dolor in reprehenderit in== voluptate [link](google.com) velit esse. `ea commodo consequat`. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.

> sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. 


```python
import os
import torch
import torch.optim as optim
import torch.nn.functional as F


def train(rank, args, model, device, dataset, dataloader_kwargs):
    torch.manual_seed(args.seed + rank)

    train_loader = torch.utils.data.DataLoader(dataset, **dataloader_kwargs)

    optimizer = optim.SGD(model.parameters(), lr=args.lr, momentum=args.momentum)
    for epoch in range(1, args.epochs + 1):
        train_epoch(epoch, args, model, device, train_loader, optimizer)
    return

```

This is a [link](google.com)
## All kinds of check boxes
- [ ] to-do  #task
- [/] incomplete #task
- [x] done #task
- [-]  canceled
- [>]  forwarded
- [<]  scheduling
- [?]  question
- [!]  important
- [*]  star
- ["]  quote
- [l]  location
- [b]  bookmark
- [i]  information
- [S]  savings
- [I]  idea
- [p]  pros
- [c]  cons
- [f]  fire
- [k]  key
- [w]  win
- [u]  up
- [d]  down
### The standard Lorem Ipsum passage, used since the 1500s

"Lorem ipsum dolor **sit amet, consectetur adipiscing elit**, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut *aliquip ex ea commodo consequat.* Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

# Ex debitis voluptatum aut illum veritatis. 

Lorem ipsum dolor sit amet. Ad facilis dolores _Est accusantium qui quibusdam incidunt non quae consectetur_ aut explicabo mollitia. Est ratione iusto [Eos facere et ratione magni sit consectetur porro sit autem possimus](https://www.loremipzum.com/)? Vel quia soluta in consequatur modiEt expedita nam atque dolores qui itaque mollitia cum voluptatem natus! 

-   Vel perspiciatis voluptatem eos nesciunt nisi. 
-   Ut quia minus non sequi repellat ut vero iure. 

## Sed possimus aliquid sed blanditiis amet? 

Ex omnis sunt qui ipsam adipisciNam iste. Id corrupti aspernatur _Sit amet in reprehenderit corrupti ut deserunt temporibus_. Non dolores placeat **Eos alias in obcaecati tempora non praesentium deleniti**. Est quos perferendissit temporibus quo nulla provident. 

1.  Et nesciunt sapiente qui voluptate nesciunt est vero molestiae aut totam magnam. 
2.  Ea consequatur eligendi cum dolor odio. 
3.  Et amet veniam At vitae autem non quam aliquid. 
4.  Qui itaque voluptatum ut consequuntur modi. 
5.  Qui quis eveniet ut quos nisi et aliquid nihil. 

> Hic perferendis galisum et earum adipisci et eveniet sunt sed facere atque et reiciendis voluptatem sed praesentium nihil. 

### In placeat molestiae id earum distinctio. 

Hic iste dolore non optio modiEt voluptas in molestiae saepe et eius deleniti ad repellendus eligendi aut iusto iusto. Vel animi debitis _Eos aliquam aut odio delectus vel atque tenetur_ sit repudiandae magnam in quibusdam galisum. Ut consectetur culpa aut nihil odit [Vel nemo eum magni maxime](https://www.loremipzum.com/)? Et voluptas molestiae et vitae pariaturIn ducimus sed quasi mollitia 33 consequuntur animi vel animi quidem! 

**Et doloribus nihil.**
Eos illum facere et dolor commodi non iusto eius sed tenetur nihil. 

**Ut praesentium molestias.**
Sit iusto omnis quo asperiores maiores sit rerum molestiae ad neque dolores. 

**Sed quia atque eum quod neque.**
Ut maiores quod aut eveniet fuga eum magnam architecto. 

**Id vero maxime et odio ipsa.**
A sapiente voluptatem ea nihil dolorem et sint saepe. 

```python
import os
import torch
import torch.optim as optim
import torch.nn.functional as F

def train(rank, args, model, device, dataset, dataloader_kwargs):
    torch.manual_seed(args.seed + rank)
```