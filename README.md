# FastAPI by Silabuz

## Query param: URL
silabuz.com/?search=sillas&status=good
-> Query params:
```
{
    search: sillas,
    status: good
}
```

## Path param: URL
silabuz.com/{id}/buscar

## Mezclando el Query y Path params.
silabuz.com/{name}/{status}?fecha=2022-08-01

## Body params: BODY