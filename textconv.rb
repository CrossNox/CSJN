require 'yomu'

def convert_save(file)
	puts "extrayendo texto del tomo de fallos #{file}"
	text = Yomu.new("fallos/#{file}.pdf").text
	File.open("fallos_txt/#{file}.txt","w") {|f| f.write text}
end

files = `ls 'fallos' | grep pdf`
files = files.split('.pdf').map(&:strip)
files.each do |f|
	next if f.empty?
	next if not File.file?("fallos/#{f}.pdf")
	convert_save f
end
