package MyPerlObject;

use Carp; # Give full stack error messages. 
use Data::Dumper; 
use strict; 

#
# Roger D. Pease rogerpease@gmail.com
#
#  This is meant to show you the approach I take to programming. 
#  I wrote this myself, obviously borrowing from multiple sources over the years. :)  
#

#
#
#  perl PerlObjectOutline.pm    <== Run Test process.  
#
#

sub new 
{

	my $package = shift; 
	my %options = @_; 
	my %hash = ();
	my $self = \%hash; 

	# If there were any Object specific initializetion it'd go here. 
	foreach my $variable (keys %options)
	{ 
		$self->{$variable} = $options{$variable}; 
	} 

	return bless $self, $package; 


}


#
# Handle unnamed functions (so you can call variable "Hello" as $object->Hello(); 
#
sub AUTOLOAD :lvalue
{
	my $self = shift; 
	our $AUTOLOAD; 	
	my $varName = $AUTOLOAD; $varName =~ s=MyPerlObject::==g; 	
	if ($varName eq "DESTROY") { }   #Destructor 
	elsif (! defined $self->{$varName}) 
	{
		confess "MyPerlObject: $varName not found"; 
	}	
	$self->{$varName};    # LValue means this can be assigned to. 
}


#
# Practically everything I write includes a testprocess so I can quickly re-evaluate/reformat if I need to. 
#
sub assert { my ($a,$b) = @_; if ($a) {} else { confess "$b";  } }

#
#  I am a huge Test Driven Development fan. 
#
sub TestProc
{


	#
	# This provides us free documentation and a test harness in case we choose to refactor anything. 
	#

	my $object = new MyPerlObject(Hello => 1); 
	assert(($object->Hello == 1),Dumper($object)); 
	$object->Hello = 23; 
	assert(($object->Hello == 23),Dumper($object)); 
	
	# The more we can check here the less we need to check when the whole program is woven together. 


}

TestProc() unless caller;   # Call my test proc if I call from command line. Otherwise, if called from another perl program it'll be ignored. 

1;
