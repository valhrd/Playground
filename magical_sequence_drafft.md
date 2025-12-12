# Overview
This will mainly be going through each step presented by the editorial which to me was extremely unclear and worded poorly at first glance. This will hopefully give a better idea of what it was trying to convey.

## Clarification of Problem Statement
The problem presents us with 3 quantities:
- `m` - Size of the magic sequence
- `k` - Resulting set bits we must achieve after doing a special sum
- `nums` - The 0-indexed array of numbers we get to choose from

If we let `n = len(nums)`, the entries of a magical sequence are the indices (ranging from `0` to `n - 1`).

The problem however does not fully demonstrate that indices can be repeated.

For example, suppose:
`nums = [1,2,3,4,5]`, `m = 2`, `k = 1`. Then the magical sequences that satisfy `m` and `k` are:
```
[0,0], [1,1], [2,2], [3,3], [4,4]
```
Since all sequences contain `m` entries and when doing the special sum we get a result with only one set bit. Hence the answer to this combination of inputs is:
$$1^2 + 2^2 + 3^2 + 4^2 + 5^2 = 55$$

Now that we understand this, we will go through the editorial's explanation.

## Initial Analysis of Problem
First, suppose we have an array of integers $\text{nums}$ of length $n$, and we create a sequence $S$ of size $m$. By their definition, $\text{prod}(S)$ is:

$$\text{prod}(S) = \Pi_{t \in S} \text{nums}[t]$$

Note $0 \le t < n$ since each element of $S$ is the index of an element in the array $\text{nums}$.

We now define $r_t$ to be the count of an index $t$ in $S$. For example, if:
$$\text{nums} = [0,0,2,2,4]$$

Then we have 2 0's, 0 1's, 2 2's, 0 3's, 1 4 and so on. In other words:
$$r_0 = 2, r_1 = 0, r_2 = 2, r_3 = 0, r_4 = 1, ...$$

Since $r_t$ is the count of each index and $t$ is upperbounded by $n - 1$, the following holds for every sequence $S$ that we construct:
$$\Sigma_{t=0}^{n - 1}r_t = m$$

And the product can be rewritten as follows:
$$\text{prod}(S) = \Pi_{t=0}^{n-1}\text{nums}[t]^{r_t}$$

## Repeated counting of sequences
Next, notice that for every sequence $S$, all of its unique permutations will be counted. For example, for a sequence like `[0,1,2]`, all 6 permutations are counted since they look distinct from one another:
```
[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]
```

But for `[1,1,2]`, only the following 3 are counted since swapping the ones creates duplicates:
```
[1,1,2], [1,2,1], [2,1,1]
```

So to find the number of distinct permutations, we divide the total permutations of $S$ by the product of the individual permutations:
$$\text{distinct\_perms} = \frac{m!}{\Pi_{t=0}^{n-1} r_t!}$$

Since each distinct permutation has the same product (multiplication is commutative), the total value associated with some sequence $S$ is:
$$\text{Total} = \frac{m!}{\Pi_{t=0}^{n-1} r_t!} \times \Pi_{t=0}^{n-1}\text{nums}[t]^{r_t} = m! \times \Pi_{t=0}^{n-1}\frac{\text{nums}[t]^{r_t}}{r_t!}$$

Additionally, we can identify each set of distinct permutations for a sequence $S$ using the element that has its indices in order. Fot example:
```
[0,1,2] identifies the set of sequences {[0,1,2], [0,2,1], [1,0,2], [1,2,0], [2,0,1], [2,1,0]}
``` 
and
```
[1,1,2] identifies {[1,1,2], [1,2,1], [2,1,1]}
```

## Dynamic Programming Segment
We first consider a function $h(i,j,p')$ where:
- $i$ is the largest index we can choose
- $j$ is the number of indices we are choosing
- $p'$ will be defined as $\Sigma_{t \in S}2^t$

Note by these definitions that $0 \le i \le n - 1$ and $0 \le j \le m$.

### Example
Let $\text{nums} = [1,1,1,2,2,2,3,3]$, $i = 4$ and $j = 5$. This means we can only pick an index from 0 to 4 inclusive and we must pick 5 such indices. So one possible sequence of indices would be:
```
[0,0,2,2,4]
```
which corresponds to the array of numbers:
```
[1,1,1,1,2]
```

