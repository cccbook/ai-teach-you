# 第 12 章：時空度規與克里斯多費符號

## 12.1 常見時空度規

[程式檔案：12-1-metric-christoffel.py](../_code/12/12-1-metric-christoffel.py)

```python
print("""
1. 閔考斯基度規 (平坦時空)
   ds² = -c²dt² + dx² + dy² + dz²

2. 史瓦西度規 (球對稱靜止黑洞)
   ds² = -(1-2GM/rc²)c²dt² + (1-2GM/rc²)^-1dr² + r²dΩ²

3. FLRW 度規 (宇宙學)
   ds² = -c²dt² + a(t)² [dr²/(1-kr²) + r²dΩ²]
""")
```

## 12.2 坐標系選擇

[程式檔案：12-1-metric-christoffel.py](../_code/12/12-1-metric-christoffel.py)

```python
print("""
不同坐標系：
1. 史瓦西坐標 - r = Rs 有坐標奇點
2. Eddington-Finkelstein - 穿過事件視界不會奇異
3. Kruskal-Szekeres - 整個時空可覆蓋
4. Gullstrand-Painlevé - 落體觀察者視角
""")
```
