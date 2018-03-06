class SlowNeville
    def initialize(k)
        @k = k
        @values = Array.new([[], []])
    end

    def addKey(key)
        @values[0] << key[0]
        @values[1] << key[1]

        trunc_vals = @values[1..-1]

        trunc_vals.each_with_index do |lst, idx|
            if lst.length == 2
                val = firstOrderLag(idx)

                #if lst == @values.last
                if idx == @values.length - 2
                    @values << [val]
                else
                    @values[-1] << val
                end

                @values[idx+1].delete_at(0)
            end

            if @values.length[0] == @k
                @values.each_with_index do |lst, idx|
                    @values[idx] = []
                end
            end
        end
    end

    def firstOrderLag(idx)
        j = -1
        i = j - (idx + 1)

        x1 = @values[0][i]
        x2 = @values[0][j]

        y1 = @values[idx+1][-2]
        y2 = @values[idx+1][-1]

        num = (0-x2)*y1-(0-x1)*y2
        den = x1-x2

        return Rational(num, den)
    end

    def getValues()
        return @values
    end
end

def frac_mod(frac, mod)
    num = frac.numerator % mod
    den = frac.denominator % mod

    i = 0
    z = (mod*i+num)/den

    while z != Integer(z)
        i += 1
        z = (p*i+num)/den
    end

    return z % mod
end

sn = SlowNeville.new(3)
keys = [[4, 343], [3, 431], [1, 923]]

keys.each do |key|
    sn.addKey(key)
    p sn.getValues
end

p frac_mod(sn.getValues[-1][0], 1237)
