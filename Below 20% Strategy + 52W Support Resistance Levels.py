//@version=5
indicator("Below 20% Strategy + 52W Support/Resistance Levels @FREEZRX", overlay = true)

// Inputs
posColorInput = input.color(color.new(#089981, 90), "Positive Color")
negColorInput = input.color(color.new(#f23645, 90), "Negative Color")
supportResistanceColor = input.color(color.new(color.blue, 0), "52W Support/Resistance Color")
transparencyInput = input.int(50, title="Transparency for -20% Level", minval=0, maxval=100)

// Calculating 52-Week High and Low
high52W = ta.highest(high, 52 * 5)  // 52 weeks * 5 trading days per week
low52W = ta.lowest(low, 52 * 5)

// Utility Functions
changePercentString(value, base) =>
    round = (value / base) * 100 - 100
    (round >= 0 ? "+" : "") + str.tostring(round, format.percent)

deletePastDrawings() =>
    for _label in label.all
        _label.delete()
    for _line in line.all
        _line.delete()

calcColor(price, comparedTo, transp = 0) => 
    color.new(price >= comparedTo ? posColorInput : negColorInput, transp)

// Variables globales pour Buy Price (déclaration initiale)
var float buyPrice20 = na  // Retrait de la variable 'buyPrice50'

// Drawing Function for Targets
drawTarget(price, labelText, currLine, basePrice, YearFromNow, transp=0, lineColor=color.blue) =>
    priceChange = changePercentString(price, basePrice)
    label.new(YearFromNow, price, labelText + " " + priceChange, color = calcColor(price, basePrice, transp), textcolor = color.white, xloc = xloc.bar_time, style = label.style_label_right)
    l = line.new(time, basePrice, YearFromNow, price, color = lineColor, xloc = xloc.bar_time, style = line.style_dotted)
    linefill.new(currLine, l, price > basePrice ? posColorInput : negColorInput)

// Variables pour la gestion de l'affichage
var targetShown = false
var float currentPrice = na 

// Get the current price
if not na(syminfo.target_price_date) and na(syminfo.target_price_date[1])
    targetShown := true
    currentPrice := close  // Assigner le prix actuel

    // Calculer 'YearFromNow' seulement lors de l'initialisation
    YearFromNow = syminfo.target_price_date + timeframe.in_seconds("12M") * 1000

    // Supprimer les dessins précédents
    deletePastDrawings()
    
    currLine = line.new(time, currentPrice, YearFromNow, currentPrice, xloc.bar_time, color = color.blue, style = line.style_dotted)

    // Calculer le "Buy Price" à -20% du prix actuel
    buyPrice20 := currentPrice * 0.80  // 20% de baisse par rapport au prix actuel

    // Ajouter des labels et des lignes pour le niveau -20% avec une transparence accrue
    drawTarget(buyPrice20, "BP -20%", currLine, currentPrice, YearFromNow, transparencyInput)

    // Dessiner les niveaux de support et de résistance sur 52 semaines
    drawTarget(high52W, "52W High", currLine, currentPrice, YearFromNow, 0, supportResistanceColor)
    drawTarget(low52W, "52W Low", currLine, currentPrice, YearFromNow, 0, supportResistanceColor)

    // Ajouter un tooltip pour les prévisions
    nameLabel = label.new(bar_index, currentPrice, ".", color = color.new(#2962ff, 100), style = label.style_label_center, textcolor = color.new(#2962ff, 0),
      tooltip = str.format("The analysts offering 1 year price forecasts for {0} have a maximum estimate and a minimum estimate for this stock.", syminfo.ticker))

// Si aucun niveau cible n'est affiché, afficher un avertissement
if barstate.islast and not targetShown 
    t = table.new(position.top_right, 1, 1, chart.fg_color)
    warningText = "No analyst predictions found."
    if barstate.isconfirmed    
        warningText += "\nIf there are any new predictions for this symbol, they should appear once the market opens."
    t.cell(0, 0, warningText, text_color = chart.bg_color)

// Afficher les niveaux de support et de résistance sur 52 semaines dans l'échelle des prix
plot(high52W, "52W High", color = supportResistanceColor, display = display.price_scale, linewidth=2)
plot(low52W,  "52W Low",  color = supportResistanceColor, display = display.price_scale, linewidth=2)

// Afficher le niveau de Buy Price -20% sur l'échelle des prix
plot(buyPrice20, title="BP -20%", color = calcColor(buyPrice20, currentPrice, transparencyInput), display = display.price_scale, linewidth=2)

//@FREEZRX
