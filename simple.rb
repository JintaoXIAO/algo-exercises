class Boolean < Struct.new(:value)

  def to_ruby
    "-> e { #{value.inspect} }"
  end
  def evaluate(environment)
    self
  end

  def to_s
    value.to_s
  end

  def inspect
    "#{self}"
  end

  def reducible?
    false
  end
end

class Number < Struct.new(:value)

  def to_ruby
    "-> e { #{value.inspect} }"
  end

  def evaluate(environment)
    self
  end

  def to_s
    value.to_s
  end

  def inspect
    "#{self}"
  end

  def reducible?
    false
  end
end

class Add < Struct.new(:left, :right)

  def to_ruby
    "-> e { (#{left.to_ruby}).call(e) + (#{right.to_ruby}).call(e) }"
  end

  def evaluate(environment)
    Number.new(left.evaluate(environment).value +
               right.evaluate(environment).value)
  end

  def to_s
    "#{left} + #{right}"
  end

  def inspect
    "{#{self}}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    if left.reducible?
      Add.new(left.reduce(environment), right)
    elsif right.reducible?
      Add.new(left, right.reduce(environment))
    else
      Number.new(left.value + right.value)
    end
  end
end

class Multiply < Struct.new(:left, :right)

  def to_ruby
    "-> e { (#{left.to_ruby}).call(e) * (#{right.to_ruby}).call(e) }"
  end

  def evaluate(environment)
    Number.new(left.evaluate(environment).value *
               right.evaluate(environment).value)
  end

  def to_s
    "#{left} * #{right}"
  end

  def inspect
    "{#{self}}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    if left.reducible?
      Multiply.new(left.reduce(environment), right)
    elsif right.reducible?
      Multiply.new(left, right.reduce(environment))
    else
      Number.new(left.value * right.value)
    end
  end
end

class LessThan < Struct.new(:left, :right)

  def to_ruby
    "-> e { (#{left.to_ruby}).call(e) < (#{right.to_ruby}).call(e) }"
  end

  def evaluate(environment)
    Boolean.new(left.evaluate(environment).value <
                right.evaluate(environment).value)
  end

  def to_s
    "#{left} < #{right}"
  end

  def inspect
    "#{self}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    if left.reducible?
      LessThan.new(left.reduce(environment), right)
    elsif right.reducible?
      LessThan.new(left, right.reduce(environment))
    else
      Boolean.new(left.value < right.value)
    end
  end
end

class Variable < Struct.new(:name)

  def to_ruby
    "-> e { e[#{name.inspect}] }"
  end

  def evaluate(environment)
    environment[name]
  end

  def to_s
    name.to_s
  end

  def inspect
    "#{self}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    environment[name]
  end
end

class DoNothing

  def to_ruby
    '-> e { e }'
  end

  def evaluate(environment)
    environment
  end

  def to_s
    'do-nothing'
  end

  def inspect
    "#{self}"
  end

  def ==(other_statement)
    other_statement.instance_of?(DoNothing)
  end

  def reducible?
    false
  end
end

class Assign < Struct.new(:name, :expression)

  def to_ruby
    "-> e { e.merge({ #{name.inspect} => (#{expression.to_ruby}).call(e) })}"
  end

  def evaluate(environment)
    environment.merge({ name => expression.evaluate(environment) })
  end

  def to_s
    "#{name} = #{expression}"
  end

  def inspect
    "#{self}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    if expression.reducible?
      [Assign.new(name, expression.reduce(environment)), environment]
    else
      [DoNothing.new, environment.merge({ name => expression })]
    end
  end
end

class If < Struct.new(:condition, :consequence, :alternative)

  def to_ruby
    "-> e { if (#{condition.to_ruby}).call(e)"+
      " then (#{consequence.to_ruby}).call(e)"+
      " else (#{alternative.to_ruby}).call(e)"+
      " end }"
  end

  def evaluate(environment)
    case condition.evaluate(environment)
    when Boolean.new(true)
      consequence.evaluate(environment)
    when Boolean.new(false)
      alternative.evaluate(environment)
    end
  end

  def to_s
    "if (#{condition}) { #{consequence} } else { #{alternative} }"
  end

  def inspect
    "#{self}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    if condition.reducible?
      [If.new(condition.reduce(environment), consequence, alternative), environment]
    else
      case condition
      when Boolean.new(true)
        [consequence, environment]
      when Boolean.new(false)
        [alternative, environment]
      end
    end
  end
end

class Sequence < Struct.new(:first, :second)

  def to_ruby
    "-> e { (#{second.to_ruby}).call((#{first.to_ruby}).call(e)) }"
  end

  def evaluate(environment)
    second.evaluate(first.evaluate(environment))
  end

  def to_s
    "#{first}; #{second}"
  end

  def inspect
    "#{self}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    case first
    when DoNothing.new
      [second, environment]
    else
      reduced_first, reduced_environment = first.reduce(environment)
      [Sequence.new(reduced_first, second), reduced_environment]
    end
  end
end

class While < Struct.new(:condition, :body)

  def to_ruby
    "-> e {" +
      " while (#{condition.to_ruby}).call(e); " +
      " e = (#{body.to_ruby}).call(e);" +
      " end;" +
      " e" +
      " }"
  end

  def evaluate(environment)
    case condition.evaluate(environment)
    when Boolean.new(true)
      evaluate(body.evaluate(environment))
    when Boolean.new(false)
      environment
    end
  end

  def to_s
    "while (#{condition}) { #{body} }"
  end

  def inspect
    "#{self}"
  end

  def reducible?
    true
  end

  def reduce(environment)
    [If.new(condition, Sequence.new(body, self), DoNothing.new), environment]
  end
end

class Machine < Struct.new(:statement, :environment)
  def step
    self.statement, self.environment = statement.reduce(environment)
  end

  def run
    while statement.reducible?
      puts "#{statement}, #{environment}"
      step
    end
    puts "#{statement}, #{environment}"
  end
end

# main

statement =
  While.new(
    LessThan.new(Variable.new(:x), Number.new(5)),
    Assign.new(:x, Multiply.new(Variable.new(:x), Number.new(3))))

puts statement.to_ruby
proc = eval(statement.to_ruby)
puts proc.call({x: 1})

# statement = Assign.new(:y, Add.new(Variable.new(:x), Number.new(1)))
# puts statement.to_ruby

# puts Add.new(Variable.new(:x), Number.new(1)).to_ruby

# expression = Variable.new(:x)
# puts expression
# puts expression.to_ruby
# proc = eval(expression.to_ruby)
# puts proc.call({x: 8})

# proc = eval(Number.new(5).to_ruby)
# puts proc.call({})

# proc = eval(Boolean.new(false).to_ruby)
# puts proc.call({})

# puts Number.new(5).to_ruby
# puts Boolean.new(false).to_ruby

# statement =
#   While.new(
#     LessThan.new(Variable.new(:x), Number.new(5)),
#     Assign.new(:x, Multiply.new(Variable.new(:x), Number.new(3))))

# puts statement
# puts statement.evaluate({ x: Number.new(1) })

# statement = Sequence.new(
#   Assign.new(:x, Add.new(Number.new(1), Number.new(1))),
#   Assign.new(:y, Add.new(Variable.new(:x), Number.new(3))))

# puts statement
# puts statement.evaluate({})

# puts Number.new(32).evaluate({})
# puts Variable.new(:x).evaluate({x: Number.new(23)})
# puts LessThan.new(
#        Add.new(Variable.new(:x), Number.new(2)),
#        Variable.new(:y))
#        .evaluate({x:Number.new(2), y:Number.new(54)})

# Machine.new(
#   While.new(
#     LessThan.new(Variable.new(:x), Number.new(5)),
#     Assign.new(:x, Multiply.new(Variable.new(:x), Number.new(3)))),
#   { x: Number.new(1) }
# ).run

# Machine.new(
#   Sequence.new(
#     Assign.new(:x, Add.new(Number.new(1), Number.new(1))),
#     Assign.new(:y, Add.new(Variable.new(:x), Number.new(3)))),
#     {}).run

# Machine.new(
#   If.new(Variable.new(:x), Assign.new(:y, Number.new(1)), DoNothing.new),
#   { x: Boolean.new(false) }).run

# Machine.new(
#   If.new(Variable.new(:x),
#          Assign.new(:y, Number.new(1)),
#          Assign.new(:y, Number.new(2))),
#   { x: Boolean.new(true) }).run

# Machine.new(
#   Assign.new(:x, Add.new(Variable.new(:x), Number.new(1))),
#   { x: Number.new(2) }
# ).run

# statement = Assign.new(:x, Add.new(Variable.new(:x), Number.new(1)))
# puts statement
# environment = { x: Number.new(2) }
# puts environment
# puts statement.reducible?
# statement, environment = statement.reduce(environment)
# puts [statement, environment]
# puts statement.reducible?
# statement, environment = statement.reduce(environment)
# puts [statement, environment]
# puts statement.reducible?
# statement, environment = statement.reduce(environment)
# puts [statement, environment]


# Machine.new(
#   Add.new(Variable.new(:x), Variable.new(:y)),
#   {x: Number.new(3), y: Number.new(4)}
# ).run

# Machine.new(LessThan.new(Number.new(5), Add.new(Number.new(2), Number.new#(2)))).run

# Machine.new(Add.new(Multiply.new(Number.new(1), Number.new(2)),
#                     Multiply.new(Number.new(3), Number.new(4)))).run

# puts Add.new(Multiply.new(Number.new(1), Number.new(2)),
#              Multiply.new(Number.new(3), Number.new(5)))
# puts Number.new(45)
# puts Number.new(1).reducible?
# puts Add.new(Number.new(1), Number.new(3)).reducible?

# expression = Add.new(Multiply.new(Number.new(1), Number.new(2)),
#                      Multiply.new(Number.new(3), Number.new(4)))

# puts expression.reducible?
# expression = expression.reduce
# puts expression
# expression = expression.reduce
# puts expression
# expression = expression.reduce
# puts expression
